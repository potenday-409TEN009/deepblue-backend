from django.shortcuts import render
from rest_framework import generics,permissions
from backend.deepblueapp.models import Post
from backend.deepblueapp.serializers import PostSerializer

# Create your views here.
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self,serializer):
        serializer.save(user_profile = self.request.user.user_profile)
    
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_update(self, serializer):
        serializer.save(user_profile=self.request.user.user_profile)
    
