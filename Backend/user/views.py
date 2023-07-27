from rest_framework.response import Response
from rest_framework import status, viewsets, permissions

from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer, UserSerializer, UserListSerializer, UserLoginSerializer
from rest_framework.permissions import BasePermission
from .models import User


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_permission_object(self, request, view, obj):
        return obj == request.user


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


class UserViewset(viewsets.ModelViewSet):
    http_method_names = ["get", "put", "delete"]
    serializer_class = UserSerializer
    queryset = User
    permission_classes = [UserPermission]

    def get_permissions(self):
        return super().get_permissions()

    def list(self, request):
        if not request.user.is_admin:
            return Response("not allowed", status=status.HTTP_403_FORBIDDEN)

        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRegistrationViewset(viewsets.ModelViewSet):
    serializer_class = UserRegistrationSerializer
    http_method_names = ["post"]
