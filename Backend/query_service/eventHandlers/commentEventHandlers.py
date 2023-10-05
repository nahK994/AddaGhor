from .commonCodes import *
from timeline.models import Comment, Post
from user.models import User


def commentCreateEventHandler(data):
    filtered_user = User.objects.filter(id=data['user'])
    filtered_post = Post.objects.filter(id=data['post'])
    Comment.objects.create(id=data['id'], text=data['text'], user=filtered_user[0], post=filtered_post[0])


def commentUpdateEventHandler(data):
    filtered_comment_obj = Comment.objects.filter(id=data['id'])
    if not filtered_comment_obj:
        return
    filtered_comment_obj.update(text=data['text'])


def commentDeleteEventHandler(data):
    filtered_comment_obj = Comment.objects.filter(id=data['id'])
    if not filtered_comment_obj:
        return
    filtered_comment_obj[0].delete()
    