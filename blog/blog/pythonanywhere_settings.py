"""
Configuración de Django para PythonAnywhere - CineForo
"""

from .settings import *
from decouple import config

# ===== SEGURIDAD =====
DEBUG = False
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = [config('PYTHONANYWHERE_DOMAIN')]  # ej: tuusuario.pythonanywhere.com

# HTTPS settings (PythonAnywhere maneja SSL automáticamente)
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# ===== BASE DE DATOS PYTHONANYWHERE (MySQL) =====
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),  # tuusuario$cineforo
        'USER': config('DB_USER'),  # tuusuario
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),  # tuusuario.mysql.pythonanywhere-services.com
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# ===== ARCHIVOS ESTÁTICOS PYTHONANYWHERE =====
# PythonAnywhere los sirve automáticamente
STATIC_ROOT = config('STATIC_ROOT')  # /home/tuusuario/mysite/static
MEDIA_ROOT = config('MEDIA_ROOT')    # /home/tuusuario/mysite/media
MEDIA_URL = '/media/'

# ===== CACHE SIMPLE =====
# Sin Redis en planes básicos
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'cineforo-cache',
    }
}

# ===== EMAIL =====
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default=None)
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default=None)
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@cineforo.com')

# ===== LOGGING =====
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': config('LOG_FILE', default='/home/tuusuario/mysite/logs/django.log'),
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# ===== OPTIMIZACIONES =====
DATABASES['default']['CONN_MAX_AGE'] = 60

print("🚀 CineForo configurado para PythonAnywhere") 