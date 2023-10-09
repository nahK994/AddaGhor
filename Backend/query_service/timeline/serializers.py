from rest_framework import serializers
from .models import Comment, Post


class PostQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = []

    def to_representation(self, instance):
        return {
            "postId": instance.id,
            "text": instance.text,
            "date": instance.date.strftime("%D"),
            "author": {
                "profilePic": None,
                "name": instance.user.name,
                "userId": instance.user.id
            }
        }


class CommentQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = []

    def to_representation(self, instance):
        return {
            "commentId": instance.id,
            "text": instance.text,
            "date": instance.date.strftime("%D"),
            "author": {
                "profilePic": None,
                "name": instance.user.name,
                "userId": instance.user.id
            }
        }