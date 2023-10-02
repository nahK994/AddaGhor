import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "App.settings_local")
django.setup()


from .models import User, UserProfile


def userCreateEventHandler(data):
    user_obj = User.objects.create_user(data['id'] ,data['name'], data['email'], data['password'])
    UserProfile.objects.create(
        id=data['userProfileId'],
        user=user_obj,
        bio=data['bio'],
        profile_picture=data['profilePicture']
    )


def userUpdateEventHandler(data):
    filtered_user_obj = User.objects.filter(id=data['id'])
    if not filtered_user_obj:
        return

    filtered_user_obj.update(name=data['name'])
    # user_obj.set_password(data['password'])
    filtered_user_profile = UserProfile.objects.filter(user=filtered_user_obj[0])    
    filtered_user_profile.update(
        user=filtered_user_obj[0],
        bio=data['bio'],
        profile_picture=data['profilePicture']
    )


def userDeleteEventHandler(data):
    filtered_user_obj = User.objects.filter(id=data['id'])
    if not filtered_user_obj:
        return
    filtered_user_obj[0].user_profile.all().delete()
    filtered_user_obj.delete()
    