from rest_framework.response import Response
from rest_framework import status, viewsets

from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, UserRegistrationSerializer, UserSerializer, UserListSerializer
from rest_framework.permissions import BasePermission
from .models import UserActivationLog, User
from rest_framework.decorators import action
from publisher.publisher import publish_user, ActionType


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

    def list(self, request):
        if not request.user.is_admin:
            return Response("not allowed", status=status.HTTP_403_FORBIDDEN)

        users = self.queryset
        serializer = UserListSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        user = request.user
        user_profile = user.user_profile.all()
        publish_user(ActionType.delete, user_profile[0])
        user_profile.delete()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserRegistrationViewset(viewsets.ModelViewSet):
    serializer_class = UserRegistrationSerializer
    http_method_names = ["post"]


class UserActivationViewset(viewsets.ViewSet):

    @action(methods=['put'], detail=True, url_path='activate')
    def activate_user(self, request, pk=None):
        activation_code = request.query_params['code']
        filtered_user_activation_log = UserActivationLog.objects.prefetch_related('user', 'user__user_profile').filter(user=pk)
        if not filtered_user_activation_log:
            return Response({
                "message": "You are not registered yet."
            })
        user_activation_log = filtered_user_activation_log[0]
        
        if user_activation_log.activation_code == activation_code:
            user = user_activation_log.user
            user_profile = user.user_profile.all()[0]
            user_profile.is_verified = True
            user_profile.save()
            response_dict = {
                "userId": user.id,
                "name": user.name,
                "email": user.email,
                "bio": user_profile.bio
            }
            publish_user(ActionType.post, user_profile)
            return Response(response_dict, status=200)
        else:
            return Response("user cannot be activated", status=403)
