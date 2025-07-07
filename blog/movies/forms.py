from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Review, Comment

class ReviewForm(forms.ModelForm):
    content = forms.CharField(
        widget=CKEditor5Widget(config_name='default'),
        label="Tu reseña",
        help_text="Comparte tu experiencia detallada. Usa negritas, listas y emojis.",
    )
    
    has_spoilers = forms.BooleanField(
        required=False,
        label="⚠️ Mi reseña contiene spoilers",
        help_text="Marca si revelas elementos importantes de la trama"
    )
    
    class Meta:
        model = Review
        fields = ['title', 'content', 'rating', 'has_spoilers']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Una obra maestra del cine moderno',
                'maxlength': 200
            }),
            'rating': forms.RadioSelect(attrs={'class': 'rating-radio'}),
        }
        labels = {
            'title': 'Título de tu reseña',
            'rating': 'Tu calificación',
        }

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=CKEditor5Widget(config_name='comment'),
        label="Tu comentario",
        help_text="Comparte tu opinión sobre esta reseña."
    )
    
    has_spoilers = forms.BooleanField(
        required=False,
        label="⚠️ Contiene spoilers",
        help_text="Marca si revelas elementos de la trama"
    )
    
    class Meta:
        model = Comment
        fields = ['content', 'has_spoilers'] 