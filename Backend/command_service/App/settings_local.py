from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'command_db_adda_ghor',
        'USER': 'skhan',
        'PASSWORD': 'haha',
        'HOST': 'command_db',
        'PORT': '5432',
    }
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200"
]
