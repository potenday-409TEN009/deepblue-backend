
from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permission import IsOwnerOrReadOnly
from rest_framework.response import Response
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user.userprofile)
    def get_queryset(self):
        queryset = Post.objects.all()
        category = self.request.query_params.get('category', None)
        post_type = self.request.query_params.get('type', None)

        #defalut 값설정
        if category not in ['a', 'b', 'c']:
            category = None
        if post_type not in ['realtime', 'best']:
            post_type = None

        if category:
            queryset = queryset.filter(category=category)

        if post_type == 'realtime':
            queryset = queryset.order_by('-created_at')
        elif post_type == 'best':
            # Assuming 'likes' field exists. If not, you need to implement a way to determine 'best' posts
            queryset = queryset.order_by('-likes')

        return queryset[:3]  # Return only 3 posts

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
