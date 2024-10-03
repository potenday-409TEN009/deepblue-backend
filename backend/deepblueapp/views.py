from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRankingSerializer

from .models import UserProfile

class UserRankingListView(APIView):
    def get(self, request): 
        users = UserProfile.objects.all().order_by('-score')[:100]
        serializer = UserRankingSerializer(users,many=True,context={'request':request})
        return Response(serializer.data)


