from rest_framework.response import Response
from rest_framework import status, viewsets, permissions

from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, UserProfile
from .serializers import UserProfileSerializer, UserSerializer, UserListSerializer, UserLoginSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserLoginViewset(viewsets.ModelViewSet):
    serializer_class = UserLoginSerializer
    http_method_names = ["post"]

    def create(self, request):
        filtered_user = User.objects.filter(email=request.data['email'])
        if not filtered_user:
            return Response("no such user", status=status.HTTP_403_FORBIDDEN)
        user = filtered_user[0]

        if user.check_password(request.data['password']):
            user_info = get_tokens_for_user(user)
            user_info['isAdmin'] = user.is_admin
            user_info['userId'] = user.id
            return Response(user_info, status=status.HTTP_200_OK)
        else:
            return Response("invalid email or password", status=status.HTTP_403_FORBIDDEN)


class UserViewset(viewsets.ViewSet):
    http_method_names = ["get", "put", "delete"]
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        # print(request.user)
        if not request.user.is_admin:
            return Response("not allowed", status=status.HTTP_403_FORBIDDEN)

        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        if pk != request.user.id:
            return Response({'message': 'You are not allowed to access other user details'},
                            status=status.HTTP_403_FORBIDDEN)

        filtered_user = User.objects.filter(id=pk)
        if not filtered_user:
            return Response({'message': 'no such user'}, status=status.HTTP_404_NOT_FOUND)
        user = filtered_user[0]
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        user = request.user
        if 'email' in request.data:
            filtered_user = User.objects.filter(email=request.data['email']).exclude(id=pk)
            if filtered_user:
                return Response({'message': 'Email already exists'}, status=status.HTTP_403_FORBIDDEN)

        user.email = request.data['email']
        user.name = request.data['name']

        if 'password' in request.data:
            user.set_password(request.data['password'])
        user.save()
        serialized_user = UserSerializer(user)
        return Response(serialized_user.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        if not request.user.is_admin:
            return Response("not allowed", status=status.HTTP_403_FORBIDDEN)

        filtered_user = User.objects.filter(id=pk)
        if not filtered_user:
            return Response("no such user", status=status.HTTP_404_NOT_FOUND)
        user = filtered_user[0]

        user.delete()
        return Response("user deleted", status=status.HTTP_200_OK)


class UserRegistrationViewset(viewsets.ViewSet):
    http_method_names = ["post"]

    def create(self, request):
        try:
            data = request.data
            if len(User.objects.filter(email=data['email'])):
                return Response({'message': 'Email already exists'}, status=status.HTTP_403_FORBIDDEN)

            user_obj = User.objects.create_user(data['name'], data['email'], data['password'])

            user_profile_obj = UserProfile.objects.create(
                user=user_obj,
                bio=data['bio'],
                profile_picture=data['profilePicture']
            )
            user_profile_serializer = UserProfileSerializer(user_profile_obj, context={'request': request})

            return Response(user_profile_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
