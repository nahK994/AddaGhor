from .settings import *
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': 'query_db',
        'PORT': '5432',
    }
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200"
]
