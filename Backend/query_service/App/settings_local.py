from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'query_db_adda_ghor',
        'USER': 'skhan',
        'PASSWORD': 'haha',
        'HOST': '0.0.0.0',
        'PORT': '5001',
    }
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200"
]
