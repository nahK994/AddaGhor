from rest_framework import serializers
from .models import Post


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
    

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "text": instance.text,
            "date": instance.date.strftime("%D")
        }