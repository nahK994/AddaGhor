from rest_framework import serializers
from .models import User, UserProfile
from publisher.publisher import publish_user, ActionType


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


    def update(self, instance, validated_data):
        if 'email' in validated_data:
            filtered_user = User.objects.filter(email=validated_data['email'])
            if filtered_user and filtered_user[0] != instance:
                raise serializers.ValidationError('Email already exists')

        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()

        if instance.user_profile.all():
            user_profile = instance.user_profile.all()[0]
            user_profile.bio = validated_data.get('bio', user_profile.bio)
            user_profile.save()

        publish_user(ActionType.put, instance.user_profile.all()[0])

        return instance


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


class UserRegistrationSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.CharField()
    bio = serializers.CharField()
    password = serializers.CharField()
    profilePicture = serializers.CharField(required=False)

    def create(self, validated_data):
        data = validated_data
        if 'profilePicture' not in data:
            data['profilePicture'] = None

        user_obj = User.objects.create_user(data['name'], data['email'], data['password'])
        user_profile_obj = UserProfile.objects.create(
            user=user_obj,
            bio=data['bio'],
            profile_picture=data['profilePicture']
        )
        user_profile_obj.user.password = data['password']
        publish_user(ActionType.post, user_profile_obj)
        
        return user_profile_obj
    
    def to_representation(self, instance):
        return {
            "userId": instance.user.id,
            "name": instance.user.name,
            "email": instance.user.email,
            "bio": instance.bio
        }
