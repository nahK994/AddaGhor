from django.shortcuts import render
from rest_framework import status, viewsets
from timeline.serializers import PostSerializer


# Create your views here.
class PostViewset(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    http_method_names = ["post"]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
