from django.shortcuts import render
from rest_framework import status, viewsets
from timeline.serializers import PostSerializer
from rest_framework.permissions import BasePermission, IsAuthenticated
from .models import Post
from rest_framework.response import Response


class PostCommandPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class PostViewset(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    http_method_names = ["post", "put", "get"]
    queryset = Post.objects.prefetch_related('user').all()


    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action == 'update' or self.action == 'destroy':
            permission_classes.append(PostCommandPermission)

        return [permission() for permission in permission_classes]


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    
    def list(self, request, *args, **kwargs):
        posts = self.queryset.filter(user=request.user)
        serialized_data = PostSerializer(posts, many=True).data
        return Response(serialized_data, status=status.HTTP_200_OK)

    
    def retrieve(self, request, pk):
        post = self.queryset.filter(id=pk)
        serialized_data = PostSerializer(post).data
        return Response(serialized_data, status=status.HTTP_200_OK)
