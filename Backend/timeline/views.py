from rest_framework import viewsets
from .serializers import CommentSerializer, PostSerializer
from rest_framework.permissions import BasePermission, IsAuthenticated
from .models import Comment, Post, React
from rest_framework.decorators import action
from rest_framework.response import Response


class ReactType:
    smile = 'smile'
    love = 'love'
    like = 'like'


class CommandPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class PostViewset(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.prefetch_related('user').all()

    def get_permissions(self):
        if self.action in ['update', 'destroy', ReactType.love, ReactType.like, ReactType.smile]:
            permission_classes = [CommandPermission]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    
    @action(methods=['put'], detail=True, url_path=ReactType.smile, url_name=ReactType.smile)
    def smile(self, request, pk):
        post = self.get_object()
        react = React.objects.filter(user=request.user)
        if not react:
            react = React.objects.create(
                user = request.user,
                post = post,
                smile=1
            )
            return Response("success", status=200)
        elif not react[0].smile:
            react.update(
                smile=1,
                love=0,
                like=0
            )
            return Response("success", status=200)
        else:
            react[0].delete()
            return Response("removed", status=204)
    
    @action(methods=['put'], detail=True, url_path=ReactType.love, url_name=ReactType.love)
    def love(self, request, pk):
        post = self.get_object()
        react = React.objects.filter(user=request.user)
        if not react:
            react = React.objects.create(
                user = request.user,
                post = post,
                love=1
            )
            return Response("success", status=200)
        elif not react[0].love:
            react.update(
                smile=0,
                love=1,
                like=0
            )
            return Response("success", status=200)
        else:
            react[0].delete()
            return Response("removed", status=204)
    
    @action(methods=['put'], detail=True, url_path=ReactType.like, url_name=ReactType.like)
    def like(self, request, pk):
        post = self.get_object()
        react = React.objects.filter(user=request.user)
        if not react:
            react = React.objects.create(
                user = request.user,
                post = post,
                like=1
            )
            return Response("success", status=200)
        elif not react[0].like:
            react.update(
                smile=0,
                love=0,
                like=1
            )
            return Response("success", status=200)
        else:
            react[0].delete()
            return Response("removed", status=204)


class CommentViewset(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    http_method_names = ["post", "put", "delete", "get"]
    queryset = Comment.objects.prefetch_related('post').all()

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action == 'update' or self.action == 'destroy':
            permission_classes.append(CommandPermission)

        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
