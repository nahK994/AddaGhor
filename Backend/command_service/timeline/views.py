from rest_framework import viewsets
from .serializers import CommentCommandSerializer, CommentQuerySerializer, PostCommandSerializer, PostQuerySerializer
from rest_framework.permissions import BasePermission, IsAuthenticated
from .models import Comment, Post, React
from user.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from publisher.publisher import ActionType, publish_post, publish_comment, publish_react


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
        react = React.objects.create(
            user = user,
            post = post,
            type = react_type
        )
        return react
    
    def process_react(self, react_type: str, request, pk: int):
        filtered_posts = Post.objects.filter(id=pk)
        if not filtered_posts:
            return Response("no such post", 404)
        post = filtered_posts[0]
        filtered_react = React.objects.filter(user=request.user, post=post)
        if filtered_react:
            react = filtered_react[0]
            if react.type == react_type:
                publish_react(ActionType.delete, react)
                react.delete()
                return Response("removed", status=204)
            else:
                filtered_react.update(type = react_type)
                publish_react(ActionType.put, react)
                return Response(react.id, status=200)
        else:
            created_react = self.create_post_react(user=request.user, post=post, react_type=react_type)
            publish_react(ActionType.post, created_react)
            return Response(created_react.id, status=200)

    @action(methods=['put'], detail=True, url_path=ReactType.smile, url_name=ReactType.smile)
    def smile(self, request, pk):
        return self.process_react(ReactType.smile, request, pk)
    
    @action(methods=['put'], detail=True, url_path=ReactType.love, url_name=ReactType.love)
    def love(self, request, pk):
        return self.process_react(ReactType.love, request, pk)
    
    @action(methods=['put'], detail=True, url_path=ReactType.like, url_name=ReactType.like)
    def like(self, request, pk):
        return self.process_react(ReactType.like, request, pk)


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
    
    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        publish_post(ActionType.delete, post)
        post.delete()
        return Response(status=204)


class CommentViewset(viewsets.ModelViewSet):
    http_method_names = ["post", "put", "get", "delete"]
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return CommentCommandSerializer
        else:
            return CommentQuerySerializer

    queryset = Comment.objects.prefetch_related('post').order_by("-date").all()
    permission_classes = [CommandPermission]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    
    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        publish_comment(ActionType.delete, comment)
        comment.delete()
        return Response(status=204)

