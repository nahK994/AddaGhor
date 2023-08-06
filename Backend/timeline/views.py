from django.shortcuts import render
from rest_framework import status, viewsets
from timeline.serializers import PostSerializer
from rest_framework.permissions import BasePermission, IsAuthenticated
from .models import Post


class PostCommandPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        data = request.data
        post = Post.objects.prefetch_related('user').filter(id=data['id'])
        return post[0].user == request.user


class PostViewset(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    http_method_names = ["post"]


    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action == 'update' or self.action == 'destroy':
            permission_classes.append(PostCommandPermission)

        return [permission() for permission in permission_classes]


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
