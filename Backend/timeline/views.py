from rest_framework import viewsets
from .serializers import CommentSerializer, PostSerializer
from rest_framework.permissions import BasePermission, IsAuthenticated
from .models import Comment, Post, React
from user.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models.query import QuerySet
from django.db.models import Prefetch


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

    def update_post_react(self, react: QuerySet, like: int = 0, smile: int = 0, love: int = 0):
        react.update(
            smile=smile,
            love=love,
            like=like
        )
    
    def create_post_react(self, user: User, post: Post, like: int = 0, smile: int = 0, love: int = 0):
        React.objects.create(
            user = user,
            post = post,
            smile=smile,
            love=love,
            like=like
        )
    
    @action(methods=['put'], detail=True, url_path=ReactType.smile, url_name=ReactType.smile)
    def smile(self, request, pk):
        post = self.get_object()
        react = React.objects.filter(user=request.user)
        if react:
            if react[0].smile:
                react[0].delete()
                return Response("removed", status=204)
            else:
                self.update_post_react(react, smile=1)
                return Response("success", status=200)
        else:
            self.create_post_react(user=request.user, post=post, smile=1)
            return Response("success", status=200)
    
    @action(methods=['put'], detail=True, url_path=ReactType.love, url_name=ReactType.love)
    def love(self, request, pk):
        post = self.get_object()
        react = React.objects.filter(user=request.user)
        if react:
            if react[0].love:
                react[0].delete()
                return Response("removed", status=204)
            else:
                self.update_post_react(react, love=1)
                return Response("success", status=200)
        else:
            self.create_post_react(user=request.user, post=post, love=1)
            return Response("success", status=200)
    
    @action(methods=['put'], detail=True, url_path=ReactType.like, url_name=ReactType.like)
    def like(self, request, pk):
        post = self.get_object()
        react = React.objects.filter(user=request.user)
        if react:
            if react[0].like:
                react[0].delete()
                return Response("removed", status=204)
            else:
                self.update_post_react(react, like=1)
                return Response("success", status=200)
        else:
            self.create_post_react(user=request.user, post=post, like=1)
            return Response("success", status=200)


class CommentViewset(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
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


class ActivityViewset(viewsets.ViewSet):
    # permission_classes = [IsAuthenticated]

    def list(self, request):
        posts = Post.objects.prefetch_related('reacts').all()
        activities = []
        for post in posts:
            activities.append({
                "post": PostSerializer(post).data,
                "comments": CommentSerializer(post.comments, many=True).data,
                "react": {
                    "love": 0,
                    "like": 0,
                    "smile": 0
                } 
            })
        return Response(activities, status=200)
