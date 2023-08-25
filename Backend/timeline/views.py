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
        if self.action in ['update', 'destroy']:
            permission_classes = [CommandPermission]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    
    def create_post_react(self, user: User, post: Post, react_type: str):
        React.objects.create(
            user = user,
            post = post,
            type = react_type
        )
    
    @action(methods=['put'], detail=True, url_path=ReactType.smile, url_name=ReactType.smile)
    def smile(self, request, pk):
        post = self.get_object()
        react = React.objects.filter(user=request.user, post=post)
        if react:
            if react[0].type == ReactType.smile:
                react[0].delete()
                return Response("removed", status=204)
            else:
                react.update(type = ReactType.smile)
                return Response("success", status=200)
        else:
            self.create_post_react(user=request.user, post=post, react_type=ReactType.smile)
            return Response("success", status=200)
    
    @action(methods=['put'], detail=True, url_path=ReactType.love, url_name=ReactType.love)
    def love(self, request, pk):
        post = self.get_object()
        react = React.objects.filter(user=request.user, post=post)
        if react:
            if react[0].type == ReactType.love:
                react[0].delete()
                return Response("removed", status=204)
            else:
                react.update(type = ReactType.love)
                return Response("success", status=200)
        else:
            self.create_post_react(user=request.user, post=post, react_type=ReactType.love)
            return Response("success", status=200)
    
    @action(methods=['put'], detail=True, url_path=ReactType.like, url_name=ReactType.like)
    def like(self, request, pk):
        post = self.get_object()
        react = React.objects.filter(user=request.user, post=post)
        if react:
            if react[0].type == ReactType.like:
                react[0].delete()
                return Response("removed", status=204)
            else:
                react.update(type = ReactType.like)
                return Response("success", status=200)
        else:
            self.create_post_react(user=request.user, post=post, react_type=ReactType.like)
            return Response("success", status=200)


class CommentViewset(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.prefetch_related('post').all()
    permission_classes = [CommandPermission]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class ActivityViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        posts = Post.objects.prefetch_related(Prefetch('reacts'), Prefetch('comments')).all()
        activities = []
        for post in posts:
            activities.append({
                "post": PostSerializer(post).data,
                "comments": CommentSerializer(post.comments, many=True).data,
                "react": {
                    "love": post.reacts.filter(type=ReactType.love).count(),
                    "like": post.reacts.filter(type=ReactType.like).count(),
                    "smile": post.reacts.filter(type=ReactType.smile).count()
                } 
            })
        return Response(activities, status=200)
