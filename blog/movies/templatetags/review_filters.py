from django import template
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def smart_preview(content, max_words=30):
    """
    Genera un preview inteligente limpiando HTML y manteniendo formato básico
    """
    if not content:
        return ""
    
    # Limpiar HTML pero mantener estructura básica
    # Convertir <p> y <br> a espacios/saltos
    content = re.sub(r'<p[^>]*>', '\n', content)
    content = re.sub(r'</p>', '\n', content)
    content = re.sub(r'<br[^>]*/?>', '\n', content)
    
    # Mantener negritas e itálicas como texto simple
    content = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', content)
    content = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', content)
    content = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', content)
    content = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', content)
    
    # Eliminar resto de HTML
    content = strip_tags(content)
    
    # Limpiar espacios extra y saltos de línea
    content = re.sub(r'\n+', ' ', content)
    content = re.sub(r'\s+', ' ', content)
    content = content.strip()
    
    # Truncar palabras
    words = content.split()
    if len(words) > max_words:
        content = ' '.join(words[:max_words]) + '...'
    
    return content

@register.filter
def spoiler_preview(review, max_words=30):
    """
    Genera preview con manejo inteligente de spoilers
    """
    if not review:
        return ""
    
    if review.has_spoilers:
        # Para reseñas con spoilers, mostrar solo advertencia
        return mark_safe(
            '<span style="color: #e67e22; font-style: italic;">'
            '<i class="fas fa-exclamation-triangle"></i> '
            'Esta reseña contiene spoilers - '
            '<strong>haz click para leer</strong>'
            '</span>'
        )
    else:
        # Para reseñas sin spoilers, mostrar preview normal
        return smart_preview(review.content, max_words)

@register.filter  
def safe_truncate_words(content, max_words=30):
    """
    Trunca palabras de contenido HTML de forma segura
    """
    if not content:
        return ""
    
    # Limpiar HTML completamente para preview
    clean_content = strip_tags(content)
    
    # Limpiar espacios extra
    clean_content = re.sub(r'\s+', ' ', clean_content).strip()
    
    words = clean_content.split()
    if len(words) > max_words:
        return ' '.join(words[:max_words]) + '...'
    
    return clean_content

@register.filter
def preview_with_spoiler_check(review, max_words=40):
    """
    Filtro principal para previews de reseñas con check de spoilers
    """
    if not review or not review.content:
        return "Sin contenido disponible"
    
    if review.has_spoilers:
        return mark_safe(
            '<div style="color: #d68910; background-color: #fff3cd; padding: 0.75rem; border-radius: 4px; border: 1px solid #d68910;">'
            '<i class="fas fa-eye-slash"></i> '
            '<strong>Contenido con spoilers</strong> - '
            'Haz click en la reseña para revelar el contenido'
            '</div>'
        )
    
    # Si no tiene spoilers, mostrar preview limpio
    preview = smart_preview(review.content, max_words)
    
    if not preview:
        return "Sin contenido para mostrar"
        
    return preview 