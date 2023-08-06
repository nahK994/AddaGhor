from django.db import models
from user.models import User


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    text = models.TextField()
    date = models.DateField(auto_now=True)

    class Meta:
        db_table = 'posts'