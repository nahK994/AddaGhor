from rest_framework import serializers
from .models import User, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email']


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length='255')
    password = serializers.CharField(max_length='500')


class UserProfileSerializer(serializers.Serializer):
    bio = serializers.CharField(max_length='500')
    profilePicture = serializers.FileField(source='profile_picture')
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['bio', 'profilePicture', 'user']
    
    def to_representation(self, instance):
        request = self.context.get('request')

        response = {
            'id': instance.id,
            'user': UserSerializer(instance.user).data,
            'bio': instance.bio,
            'profilePicture': request.build_absolute_uri(instance.profile_picture)
        }

        return response


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'is_admin']
