from rest_framework import serializers
from .models import Comment, Post


class PostSerializer(serializers.ModelSerializer):

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
            "text": instance.text,
            "date": instance.date.strftime("%D")
        }

    
class CommentCommandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = []


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
        if instance is None:
            raise serializers.ValidationError("No such item")


        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance
    

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "postId": instance.post.id,
            "text": instance.text,
            "date": instance.date.strftime("%D")
        }
