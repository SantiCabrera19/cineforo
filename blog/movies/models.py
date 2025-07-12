
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone

class Movie(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    original_title = models.CharField(max_length=200, blank=True, verbose_name="Título original")
    year = models.IntegerField(verbose_name="Año")
    director = models.CharField(max_length=100, verbose_name="Director")
    genre = models.CharField(max_length=100, verbose_name="Género")
    duration = models.IntegerField(help_text="Duración en minutos", verbose_name="Duración")
    synopsis = models.TextField(verbose_name="Sinopsis")
    poster = models.ImageField(upload_to='posters/', blank=True, null=True, verbose_name="Póster")
    imdb_rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True, verbose_name="Rating IMDb")
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Película"
        verbose_name_plural = "Películas"
        ordering = ['-created_at']
    
    # metodos especiales para el modelo
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.year}")
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return f"{self.title} ({self.year})"

class Review(models.Model):
    RATING_CHOICES = [
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
    ]
    
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews', verbose_name="Película")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor")
    title = models.CharField(max_length=200, verbose_name="Título de la reseña")
    content = models.TextField(verbose_name="Contenido")
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="Calificación")
    has_spoilers = models.BooleanField(default=False, verbose_name="Contiene spoilers")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True)
    
    class Meta:
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"
        ordering = ['-created_at']
        unique_together = ['movie', 'author']  # Un usuario solo puede hacer una reseña por película
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.author.username}")
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('review_detail', kwargs={'slug': self.slug})
    
    def get_preview(self, max_words=30):
        """Genera un preview limpio de la reseña"""
        if self.has_spoilers:
            return f"[Contenido con spoilers] - {self.title}"
        
        # Importar aquí para evitar circular imports
        from django.utils.html import strip_tags
        import re
        
        # Limpiar HTML
        clean_content = strip_tags(self.content or "")
        clean_content = re.sub(r'\s+', ' ', clean_content).strip()
        
        # Truncar palabras
        words = clean_content.split()
        if len(words) > max_words:
            return ' '.join(words[:max_words]) + '...'
        
        return clean_content
    
    def __str__(self):
        return f"Reseña de {self.movie.title} por {self.author.username}"

class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments', verbose_name="Reseña")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor")
    content = models.TextField(verbose_name="Comentario")
    has_spoilers = models.BooleanField(default=False, verbose_name="Contiene spoilers")
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies') # relacion con el mismo modelo
    
    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comentario de {self.author.username} en {self.review.title}"

class Like(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='likes', verbose_name="Reseña")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"
        unique_together = ['review', 'user']  # Un usuario solo puede dar like una vez por reseña
    
    def __str__(self):
        return f"Like de {self.user.username} en {self.review.title}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, verbose_name="Biografía")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Avatar")
    favorite_genre = models.CharField(max_length=50, blank=True, verbose_name="Género favorito")
    location = models.CharField(max_length=100, blank=True, verbose_name="Ubicación")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Fecha de nacimiento")
    
    # Configuraciones de privacidad
    show_email = models.BooleanField(default=False, verbose_name="Mostrar email en perfil público")
    show_age = models.BooleanField(default=False, verbose_name="Mostrar edad en perfil")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Perfil de usuario"
        verbose_name_plural = "Perfiles de usuario"
    
    @property # usamos property para que se pueda usar como atributo
    def age(self):
        """Calcular edad a partir de la fecha de nacimiento"""
        if self.birth_date:
            from datetime import date # importamos date para calcular la edad
            today = date.today() # fecha actual la guardamos en today
            # retornamos la edad, si la fecha de nacimiento es mayor a la fecha actual, restamos 1
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None
    
    def __str__(self):
        return f"Perfil de {self.user.username}" 