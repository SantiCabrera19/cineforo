from django.contrib import admin
from django.utils.html import format_html
from .models import Movie, Review, Comment, Like, UserProfile

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'year', 'director', 'genre', 'imdb_rating', 'created_at']
    list_filter = ['year', 'genre', 'created_at']
    search_fields = ['title', 'original_title', 'director']
    prepopulated_fields = {'slug': ('title', 'year')}
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('title', 'original_title', 'year', 'director')
        }),
        ('Detalles', {
            'fields': ('genre', 'duration', 'synopsis', 'imdb_rating')
        }),
        ('Multimedia', {
            'fields': ('poster',)
        }),
        ('Configuración', {
            'fields': ('slug', 'created_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_poster_preview(self, obj):
        if obj.poster:
            return format_html('<img src="{}" width="50" height="75">', obj.poster.url)
        return "Sin póster"
    get_poster_preview.short_description = "Vista previa"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'movie', 'author', 'rating', 'created_at']
    list_filter = ['rating', 'created_at', 'movie__genre']
    search_fields = ['title', 'movie__title', 'author__username']
    readonly_fields = ['created_at', 'updated_at', 'slug']
    
    fieldsets = (
        ('Reseña', {
            'fields': ('movie', 'author', 'title', 'content', 'rating')
        }),
        ('Metadatos', {
            'fields': ('slug', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['content_preview', 'review', 'author', 'created_at', 'parent']
    list_filter = ['created_at']
    search_fields = ['content', 'author__username', 'review__title']
    readonly_fields = ['created_at']
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = "Comentario"

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'review', 'created_at']
    list_filter = ['created_at']
    readonly_fields = ['created_at']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'favorite_genre', 'location', 'birth_date']
    list_filter = ['favorite_genre', 'location']
    search_fields = ['user__username', 'user__email', 'location']
    
    fieldsets = (
        ('Usuario', {
            'fields': ('user',)
        }),
        ('Perfil', {
            'fields': ('bio', 'avatar', 'favorite_genre', 'location', 'birth_date')
        })
    ) 