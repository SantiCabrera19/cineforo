from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count, Avg
from django.core.paginator import Paginator
from .models import Movie, Review, Comment, Like, UserProfile
from .forms import ReviewForm, CommentForm

def movie_list(request):
    """Página principal - Lista de películas con reseñas recientes"""
    movies = Movie.objects.all().order_by('-created_at')
    recent_reviews = Review.objects.select_related('movie', 'author').order_by('-created_at')[:5]
    
    # Paginación
    paginator = Paginator(movies, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'movies': page_obj,
        'recent_reviews': recent_reviews,
        'total_movies': movies.count(),
        'total_reviews': Review.objects.count(),
    }
    return render(request, 'movies/movie_list.html', context)

def movie_detail(request, slug):
    """Detalle de película con todas sus reseñas"""
    movie = get_object_or_404(Movie, slug=slug)
    reviews = movie.reviews.select_related('author').annotate(
        likes_count=Count('likes')
    ).order_by('-created_at')
    
    # Estadísticas
    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg']
    
    context = {
        'movie': movie,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'total_reviews': reviews.count(),
    }
    return render(request, 'movies/movie_detail.html', context)

def review_list(request):
    """Lista de todas las reseñas"""
    reviews = Review.objects.select_related('movie', 'author').annotate(
        likes_count=Count('likes'),
        comments_count=Count('comments')
    ).order_by('-created_at')
    
    # Filtros
    genre = request.GET.get('genre')
    rating = request.GET.get('rating')
    
    if genre:
        reviews = reviews.filter(movie__genre__icontains=genre)
    if rating:
        reviews = reviews.filter(rating=rating)
    
    # Paginación
    paginator = Paginator(reviews, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'reviews': page_obj,
        'genres': Movie.objects.values_list('genre', flat=True).distinct(),
    }
    return render(request, 'movies/review_list.html', context)

def review_detail(request, slug):
    """Detalle de reseña con comentarios"""
    review = get_object_or_404(Review.objects.select_related('movie', 'author'), slug=slug)
    comments = review.comments.select_related('author').filter(parent=None).order_by('created_at')
    
    # Verificar si el usuario ya dio like
    user_liked = False
    if request.user.is_authenticated:
        user_liked = Like.objects.filter(review=review, user=request.user).exists()
    
    # Formulario para comentarios
    comment_form = CommentForm()
    
    context = {
        'review': review,
        'comments': comments,
        'user_liked': user_liked,
        'likes_count': review.likes.count(),
        'comment_form': comment_form,
    }
    return render(request, 'movies/review_detail.html', context)

@login_required
def create_review(request, movie_slug=None):
    """Crear nueva reseña"""
    movie = None
    if movie_slug:
        movie = get_object_or_404(Movie, slug=movie_slug)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        movie_id = request.POST.get('movie')
        
        if movie_id and form.is_valid():
            try:
                selected_movie = get_object_or_404(Movie, id=movie_id)
                
                # Verificar si ya existe una reseña del usuario para esta película
                if Review.objects.filter(movie=selected_movie, author=request.user).exists():
                    messages.error(request, f'Ya has escrito una reseña para "{selected_movie.title}".')
                    raise ValueError('Review already exists')
                
                # Crear la reseña
                review = form.save(commit=False)
                review.movie = selected_movie
                review.author = request.user
                review.save()
                
                messages.success(request, f'¡Reseña de "{selected_movie.title}" creada exitosamente!')
                return redirect('movies:review_detail', slug=review.slug)
                
            except Exception as e:
                if not movie_id:
                    messages.error(request, 'Debes seleccionar una película.')
                
        # Si hay errores, volver a mostrar el formulario con datos
        context = {
            'form': form,
            'movie': movie,
            'movies': Movie.objects.all().order_by('title') if not movie else None,
            'hide_search': True,
            'form_data': {
                'title': request.POST.get('title', ''),
                'content': request.POST.get('content', ''),
                'rating': request.POST.get('rating', ''),
                'movie_id': movie_id,
                'has_spoilers': request.POST.get('has_spoilers', False),
            }
        }
        return render(request, 'movies/create_review.html', context)
    
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'movie': movie,
        'movies': Movie.objects.all().order_by('title') if not movie else None,
        'hide_search': True,
    }
    return render(request, 'movies/create_review.html', context)

def profile_view(request, username):
    """Ver perfil de usuario"""
    user = get_object_or_404(User, username=username)
    profile, created = UserProfile.objects.get_or_create(user=user)
    reviews = Review.objects.filter(author=user).order_by('-created_at')[:10]
    
    context = {
        'profile_user': user,
        'profile': profile,
        'reviews': reviews,
        'total_reviews': Review.objects.filter(author=user).count(),
    }
    return render(request, 'movies/profile_view.html', context)

@login_required
def profile_edit(request):
    """Editar mi perfil"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Actualizar datos del usuario
        user = request.user
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()
        
        # Actualizar datos del perfil
        profile.bio = request.POST.get('bio', profile.bio)[:500]  # Límite de caracteres
        profile.favorite_genre = request.POST.get('favorite_genre', profile.favorite_genre)
        
        # Manejar fecha de nacimiento
        birth_date = request.POST.get('birth_date')
        if birth_date:
            from datetime import datetime
            try:
                profile.birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
            except ValueError:
                pass
        
        # Configuraciones de privacidad
        profile.show_email = 'show_email' in request.POST
        profile.show_age = 'show_age' in request.POST
        
        profile.save()
        
        messages.success(request, '¡Perfil actualizado exitosamente! 🎬')
        return redirect('movies:profile_view', username=request.user.username)
    
    context = {'profile': profile, 'hide_search': True}
    return render(request, 'movies/profile_edit.html', context)

@login_required
def toggle_like(request, review_id):
    """Toggle like en reseña (AJAX)"""
    if request.method == 'POST':
        review = get_object_or_404(Review, id=review_id)
        like, created = Like.objects.get_or_create(review=review, user=request.user)
        
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
            
        return JsonResponse({
            'liked': liked,
            'likes_count': review.likes.count()
        })
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def add_comment(request, review_id):
    """Agregar comentario a reseña"""
    if request.method == 'POST':
        review = get_object_or_404(Review, id=review_id)
        form = CommentForm(request.POST)
        parent_id = request.POST.get('parent_id')
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.review = review
            comment.author = request.user
            if parent_id:
                comment.parent_id = parent_id
            comment.save()
            messages.success(request, 'Comentario agregado!')
        else:
            messages.error(request, 'Error al agregar comentario. Verifica el contenido.')
        
        return redirect('movies:review_detail', slug=review.slug)
    
    return redirect('movies:review_list')

def search(request):
    """Búsqueda de películas y reseñas"""
    query = request.GET.get('q', '')
    results = {'movies': [], 'reviews': []}
    
    if query:
        results['movies'] = Movie.objects.filter(
            Q(title__icontains=query) | 
            Q(director__icontains=query) |
            Q(genre__icontains=query)
        )[:10]
        
        results['reviews'] = Review.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).select_related('movie', 'author')[:10]
    
    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'movies/search.html', context)

def movie_autocomplete(request):
    """Autocomplete AJAX para buscar películas al crear reseñas"""
    query = request.GET.get('q', '').strip()
    movies = []
    
    if query and len(query) >= 2:  # Buscar solo si hay al menos 2 caracteres
        movies_queryset = Movie.objects.filter(
            Q(title__icontains=query) | 
            Q(original_title__icontains=query) |
            Q(director__icontains=query)
        ).order_by('title')[:10]  # Limitar a 10 resultados
        
        movies = [
            {
                'id': movie.id,
                'title': movie.title,
                'original_title': movie.original_title,
                'year': movie.year,
                'director': movie.director,
                'genre': movie.genre,
                'poster_url': movie.poster.url if movie.poster else None,
                'display_text': f"{movie.title} ({movie.year}) - {movie.director}"
            }
            for movie in movies_queryset
        ]
    
    return JsonResponse({'movies': movies})

def movie_by_id(request, movie_id):
    """Obtener película por ID para el autocomplete"""
    try:
        movie = Movie.objects.get(id=movie_id)
        data = {
            'id': movie.id,
            'title': movie.title,
            'original_title': movie.original_title,
            'year': movie.year,
            'director': movie.director,
            'genre': movie.genre,
            'poster_url': movie.poster.url if movie.poster else None,
        }
        return JsonResponse(data)
    except Movie.DoesNotExist:
        return JsonResponse({'error': 'Película no encontrada'}, status=404)

# ===== AUTENTICACIÓN =====

def login_view(request):
    """Vista de login para usuarios"""
    if request.user.is_authenticated:
        return redirect('movies:movie_list')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            # Crear perfil si no existe
            UserProfile.objects.get_or_create(user=user)
            
            messages.success(request, f'¡Bienvenido de vuelta, {user.username}!')
            next_url = request.GET.get('next', 'movies:movie_list')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    # Estadísticas reales del foro
    stats = {
        'total_movies': Movie.objects.count(),
        'total_reviews': Review.objects.count(),
        'total_users': User.objects.count(),
        'total_comments': Comment.objects.count(),
    }
    
    context = {'hide_search': True, 'stats': stats}
    return render(request, 'movies/auth/login.html', context)

def signup_view(request):
    """Vista de registro para nuevos usuarios"""
    if request.user.is_authenticated:
        return redirect('movies:movie_list')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Crear perfil automáticamente
            UserProfile.objects.create(user=user)
            
            # Login automático después del registro
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            
            messages.success(request, f'¡Cuenta creada exitosamente! Bienvenido, {username}!')
            return redirect('movies:movie_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserCreationForm()
    
    # Estadísticas reales del foro
    stats = {
        'total_movies': Movie.objects.count(),
        'total_reviews': Review.objects.count(),
        'total_users': User.objects.count(),
        'total_comments': Comment.objects.count(),
    }
    
    context = {'form': form, 'hide_search': True, 'stats': stats}
    return render(request, 'movies/auth/signup.html', context)

def logout_view(request):
    """Vista de logout"""
    username = request.user.username if request.user.is_authenticated else None
    logout(request)
    
    if username:
        messages.success(request, f'¡Hasta luego, {username}! Sesión cerrada exitosamente.')
    
    return redirect('movies:movie_list') 