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