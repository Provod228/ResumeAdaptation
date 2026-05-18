import os
from .base import * # Импортируем все из base.py

DEBUG = False

# Секреты ОБЯЗАТЕЛЬНО берем из переменных окружения сервера
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# На продакшене используем production-ready БД (например, PostgreSQL)
# Данные для подключения тоже берем из переменных окружения
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Дополнительная безопасность для Production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True