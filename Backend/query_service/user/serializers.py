from rest_framework import serializers
from .models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    bio = serializers.CharField()

    class Meta:
        model = User
        fields = ['name', 'email', 'bio']


    def to_representation(self, instance):
        return {
            "userId": instance.id,
            "name": instance.name,
            "email": instance.email,
            "bio": instance.user_profile.all()[0].bio
        }
