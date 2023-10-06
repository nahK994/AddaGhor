from .commonCodes import *
from timeline.models import Post, React
from user.models import User


def reactCreateEventHandler(data):
    filtered_user = User.objects.filter(id=data['user'])
    filtered_post = Post.objects.filter(id=data['post'])
    React.objects.create(id=data['id'], type=data['type'], user=filtered_user[0], post=filtered_post[0])


def reactUpdateEventHandler(data):
    filtered_react_obj = React.objects.filter(id=data['id'])
    if not filtered_react_obj:
        return
    filtered_react_obj.update(type=data['type'])


def reactDeleteEventHandler(data):
    filtered_react_obj = React.objects.filter(id=data['id'])
    if not filtered_react_obj:
        return
    filtered_react_obj[0].delete()
    