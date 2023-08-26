from rest_framework import viewsets
from .serializers import CommentSerializer, PostCommandSerializer, PostQuerySerializer
from rest_framework.permissions import BasePermission, IsAuthenticated
from .models import Comment, Post, React
from user.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
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


class ReactViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

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


class PostViewset(viewsets.ModelViewSet):
    http_method_names = ["post", "put", "get", "delete"]
    queryset = Post.objects.prefetch_related('user').order_by("-date").all()

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            permission_classes = [CommandPermission]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return PostCommandSerializer
        else:
            return PostQuerySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class CommentViewset(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.prefetch_related('post').order_by("-date").all()
    permission_classes = [CommandPermission]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class ActivityViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        posts = Post.objects.prefetch_related(Prefetch('reacts'), Prefetch('comments')).all()
        user = request.user
        activities = []
        for post in posts:
            activities.append({
                "post": PostQuerySerializer(post).data,
                "comments": CommentSerializer(post.comments, many=True).data,
                "reactCount": {
                    "love": post.reacts.filter(type=ReactType.love).count(),
                    "like": post.reacts.filter(type=ReactType.like).count(),
                    "smile": post.reacts.filter(type=ReactType.smile).count()
                },
                "userReact": post.reacts.filter(user=user)[0].type if len(post.reacts.filter(user=user)) else None
            })
        return Response(activities, status=200)
