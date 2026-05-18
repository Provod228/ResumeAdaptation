from .base import * # Импортируем все из base.py

DEBUG = True

SECRET_KEY = 'django-insecure-локальный-ключ-можно-не-прятать'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}