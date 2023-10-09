from rest_framework import viewsets
from .serializers import CommentQuerySerializer, PostQuerySerializer
from rest_framework.permissions import IsAuthenticated
from .models import Post
from rest_framework.response import Response
from django.db.models import Prefetch


class ReactType:
    smile = 'smile'
    love = 'love'
    like = 'like'

class ActivityViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def list(self, request):
        posts = Post.objects.prefetch_related(Prefetch('reacts'), Prefetch('comments')).all()
        user = request.user
        activities = []
        for post in posts:
            activities.append({
                "post": PostQuerySerializer(post).data,
                "comments": CommentQuerySerializer(post.comments, many=True).data,
                "reactCount": {
                    "love": post.reacts.filter(type=ReactType.love).count(),
                    "like": post.reacts.filter(type=ReactType.like).count(),
                    "smile": post.reacts.filter(type=ReactType.smile).count()
                },
                "userReact": post.reacts.filter(user=user)[0].type if len(post.reacts.filter(user=user)) else None
            })
        return Response(activities, status=200)
