from rest_framework import serializers
from .models import Comment, Post


class PostCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'text']
    
    def create(self, validated_data):
        request = self.context.get('request')
        data = validated_data
        post_obj = Post.objects.create(
            user = request.user,
            text = data['text']
        )
        return post_obj

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance

    def to_representation(self, instance):
        return {
            "id": instance.id,
        }


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

    
class CommentCommandSerializer(serializers.ModelSerializer):
    postId = serializers.IntegerField(required=False)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'postId']

    def validate(self, attrs):
        request = self.context.get('request')
        if request.method == "POST":
            post = Post.objects.filter(id=attrs['postId'])
            if not len(post):
                raise serializers.ValidationError("No such post")
        return attrs
    
    def create(self, validated_data):
        request = self.context.get('request')
        data = validated_data
        post = Post.objects.filter(id=validated_data['postId'])[0]
        comment_obj = Comment.objects.create(
            user = request.user,
            text = data['text'],
            post = post
        )
        return comment_obj

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance    

    def to_representation(self, instance):
        return {
            "id": instance.id,
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