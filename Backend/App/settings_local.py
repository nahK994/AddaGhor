from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'adda_ghor',
        'USER': 'skhan',
        'PASSWORD': 'haha',
        'HOST': 'db',
        'PORT': '5432',
    }
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200"
]
