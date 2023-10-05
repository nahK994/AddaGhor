from .commonCodes import *
from timeline.models import Post
from user.models import User


def postCreateEventHandler(data):
    filtered_user = User.objects.filter(id=data['user'])
    Post.objects.create(id=data['id'], text=data['text'], user=filtered_user[0])


def postUpdateEventHandler(data):
    filtered_post_obj = Post.objects.filter(id=data['id'])
    if not filtered_post_obj:
        return
    filtered_post_obj.update(text=data['text'])


def postDeleteEventHandler(data):
    filtered_post_obj = Post.objects.filter(id=data['id'])
    if not filtered_post_obj:
        return
    filtered_post_obj[0].delete()
    