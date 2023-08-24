from .base import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Email configuración
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Activa el envio de emails con dejango
# Iindicar el provedor de email
EMAIL_HOST = 'smtp.gmail.com'
# El email que envia el correo
EMAIL_HOST_USER = get_secret('EMAIL')
# Password de envio de correos para la app django tomado de google
EMAIL_HOST_PASSWORD = get_secret('PASSWORD_EMAIL')
# El puerto de envio del correo
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'default from email'

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secret('DB_NAME'),
        'USER': get_secret('USER'),
        'PASSWORD': get_secret('PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR.child('static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.child('media')