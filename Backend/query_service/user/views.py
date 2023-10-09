from rest_framework.response import Response
from rest_framework import status, viewsets

from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, UserSerializer
from .models import User
from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method.lower() == "post":
            return False
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj == request.user


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class LoginViewset(viewsets.ModelViewSet):
    http_method_names = ["post"]
    serializer_class = LoginSerializer

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
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [UserPermission]
    http_method_names = ["get"]

