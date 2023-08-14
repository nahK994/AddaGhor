from django.db import models
from user.models import User


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    text = models.TextField()
    date = models.DateField(auto_now=True)

    class Meta:
        db_table = 'posts'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    date = models.DateField(auto_now=True)

    class Meta:
        db_table = 'comments'


class React(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reacts")
    love = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    smile = models.IntegerField(default=0)

    class Meta:
        db_table = 'reacts'
