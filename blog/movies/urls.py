from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    # Página principal del foro
    path('', views.movie_list, name='movie_list'),
    
    # Películas
    path('pelicula/<slug:slug>/', views.movie_detail, name='movie_detail'),
    
    # Reseñas
    path('reseñas/', views.review_list, name='review_list'),
    path('reseña/<slug:slug>/', views.review_detail, name='review_detail'),
    path('crear-reseña/', views.create_review, name='create_review'),
    path('crear-reseña/<slug:movie_slug>/', views.create_review, name='create_review_for_movie'),
    
    # Perfiles
    path('perfil/<str:username>/', views.profile_view, name='profile_view'),
    path('mi-perfil/', views.profile_edit, name='profile_edit'),
    
    # Interacciones
    path('like/<int:review_id>/', views.toggle_like, name='toggle_like'),
    path('comentar/<int:review_id>/', views.add_comment, name='add_comment'),
    
    # Búsqueda
    path('buscar/', views.search, name='search'),
    path('api/movie-autocomplete/', views.movie_autocomplete, name='movie_autocomplete'),
    path('api/movie/<int:movie_id>/', views.movie_by_id, name='movie_by_id'),
    
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
] 