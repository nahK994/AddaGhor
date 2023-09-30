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
    TYPE = [
        ("love", "love"),
        ("like", "like"),
        ("smile", "smile")
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reacts")
    type = models.CharField(max_length=10, choices=TYPE, default=None)

    class Meta:
        db_table = 'reacts'
