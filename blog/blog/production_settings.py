"""
Configuración de Django para PRODUCCIÓN - CineForo
IMPORTANTE: Solo usar en entorno de producción.
"""

from .settings import *
from decouple import config

# ===== SEGURIDAD =====
DEBUG = False
SECRET_KEY = config('SECRET_KEY')  # OBLIGATORIO en producción
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# HTTPS settings
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# ===== BASE DE DATOS PRODUCCIÓN =====
# Ejemplo para PostgreSQL
if config('DATABASE_URL', default=None):
    import dj_database_url
    DATABASES['default'] = dj_database_url.parse(config('DATABASE_URL'))
else:
    # Configuración manual para PostgreSQL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
            'OPTIONS': {
                'sslmode': 'require',
            },
        }
    }

# ===== ARCHIVOS ESTÁTICOS =====
# Para usar con WhiteNoise o CDN
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# CDN para archivos estáticos (opcional)
if config('USE_CDN', default=False, cast=bool):
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

# ===== CACHE =====
# Redis para cache y sesiones
if config('REDIS_URL', default=None):
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': config('REDIS_URL'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    SESSION_CACHE_ALIAS = 'default'

# ===== LOGGING =====
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'logs/django_errors.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

# ===== EMAIL PRODUCCIÓN =====
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default=None)
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default=None)
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@cineforo.com')

# ===== MIDDLEWARE ADICIONAL =====
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Para archivos estáticos
] + MIDDLEWARE

# ===== OPTIMIZACIONES =====
# Compresión GZIP
USE_GZIP = True

# Optimizaciones de consulta
DATABASES['default']['CONN_MAX_AGE'] = 60

# ===== MONITOREO =====
# Sentry para monitoreo de errores
SENTRY_DSN = config('SENTRY_DSN', default=None)
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=True
    )

# ===== CONFIGURACIONES ESPECÍFICAS =====
# Límites de seguridad
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB

# Timeout para requests
DEFAULT_TIMEOUT = 30

print("🚀 Configuración de PRODUCCIÓN cargada para CineForo") 