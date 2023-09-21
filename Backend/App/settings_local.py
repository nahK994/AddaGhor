from .settings import *
from dotenv import load_dotenv
load_dotenv(dotenv_path='../.env')
import os


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'adda_ghor'),
        'USER': os.getenv('POSTGRES_USER', 'skhan'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'haha'),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

CORS_ALLOWED_ORIGINS = [
    "http://frontend:80"
]
