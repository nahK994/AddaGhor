from .settings import *
from dotenv import load_dotenv
load_dotenv(dotenv_path='../.env')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CORS_ALLOWED_ORIGINS = [
    "https://nahk994.github.io"
]
