import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "App.settings_local")
django.setup()