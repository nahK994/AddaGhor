from rest_framework import serializers
from .models import UserActivationLog, User, UserProfile
from publisher.publisher import publish_user, ActionType
from django.utils.crypto import get_random_string
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


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
            profile_picture=data['profilePicture'],
        )

        generated_activation_code = get_random_string(length=32)
        UserActivationLog.objects.create(
            user = user_obj,
            activation_code=generated_activation_code
        )

        html_content = render_to_string("user_activation_email.html", {
            "activationURL": "http://localhost:4200/user/"+str(user_obj.id)+"/activate/"+generated_activation_code
        })
        msg = EmailMultiAlternatives('User activation email', '', 'addaghor786@gmail.com', [user_obj.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
        return user_profile_obj
    
    def to_representation(self, instance):
        return {
            "message": "An activation email has been sent to your email.",
        }
