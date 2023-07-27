from .settings import *
from dotenv import load_dotenv
load_dotenv(dotenv_path='../.env')
import os


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'adda_ghor'),
        'USER': os.getenv('DB_USER', 'skhan'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'haha'),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': '5432',
    }
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
]
