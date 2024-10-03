from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.utils import timezone
from django.db.models import Count
from django.shortcuts import render
from datetime import timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import UserProfile, Post, DailyCheck, Quest, QuestList
from .serializers import UserRankingSerializer, PostSerializer, DashBoardSerializer, QuestSerializer
from .permission import IsOwnerOrReadOnly
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework.authtoken.models import Token

class UserRankingListView(APIView):
    def get(self, request): 
        users = UserProfile.objects.all().order_by('-score')[:100]
        serializer = UserRankingSerializer(users,many=True,context={'request':request})
        return Response(serializer.data)




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
            
            queryset = queryset.order_by('-likes')

        return queryset[:3] 

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DashboardAPIView(APIView):
    def get(self,request):
        user = request.user
        user_quests=Quest.objects.filter(user=user.userprofile)
        cleared_quest_count = user_quests.filter(is_cleared=True).count()
        total_cleared_day = user_quests.filter(cleared_at__isnull=False).values('cleared_at').distinct().count()
        level = user.userprofile.level
        

        today = timezone.now().date()
        start_date = today - timedelta(days=today.weekday())
        every_day=[]
        for i in range(7):
            every_day.append(start_date + timedelta(days=i))
        every_day_cleared_quest_count=[]
        for day in every_day:
            every_day_cleared_quest_count.append(user_quests.filter(cleared_at=day).count())
        
        avg_week_cleared_quest_count = sum(every_day_cleared_quest_count) / 7
        
        daily_check_count = DailyCheck.objects.filter(user=user.userprofile).count()

        data = {
            'cleared_quest_count': cleared_quest_count,
            'total_cleared_day': total_cleared_day,
            'level': level,
            'avg_week_cleared_quest': avg_week_cleared_quest_count,
            'daily_check_count': daily_check_count
        }
        serializer = DashBoardSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data,status=200)
        else:
            return Response(serializer.erros,status=400)


class UserInfoAPIView(APIView):
    def post(self, request):
        user = request.user
        data = request.data
        profile = user.userprofile

        if 'survey_level' in data:
            profile.survey_level = data['survey_level']
        elif 'nickname' in data:
            profile.nickname = data['nickname']
        elif 'survel_level' in data and 'nickname' in data:
            return Response({"error": "설문조사레벨 또는 이름중 하나만보내주세요"}, status=400)
        else:
            return Response({"error": "설문조사레벨 또는 이름을 보내주세요"}, status=400)
        profile.save()
        return Response({"message": "유저정보가 업데이트 되었습니다."}, status=200)


@api_view(['POST'])
def my_quest_create(request):
    quests_to_create =QuestList.objects.all().filter(isolation_level=request.user.isolation_level)
    for quest in quests_to_create:
        Quest.objects.create(user=request.user, difficulty=quest.difficulty, content=quest.content, score=quest.score)
    return Response(status=status.HTTP_200_OK)

class MyQuestListAPIView(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request):
        quests = []
        for difficulty in ['1', '2', '3']:
            quest = Quest.objects.filter(user=request.user, difficulty=difficulty).first()
            if quest:
                quests.append(quest)
        
        serializer = QuestSerializer(quests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MyQuestDoneAPIView(APIView):

    permission_classes = [IsAuthenticated]
    def patch(self, request):
        difficulty = request.data.get('difficulty')
        user = request.user
        quest = Quest.objects.filter(user=request.user, difficulty=difficulty).first()
        if quest:
            user.userprofile.score += quest.score
            user.userprofile.save()
            quest.is_cleared = True
            quest.save()
        return Response(status=status.HTTP_200_OK)
# Create your views here.

User = get_user_model()

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH2_REDIRECT_URI
    client_class = OAuth2Client

@api_view(['POST'])
@permission_classes([AllowAny])
def google_login(request):
    code = request.data.get('code')
    
    try:
        # Use the GoogleLogin view to handle the OAuth2 flow
        social_login_view = GoogleLogin.as_view()
        response = social_login_view(request._request)

        if response.status_code == 200:
            user = response.user
            
            # Check if the user is newly created
            is_new_user = user.date_joined == user.last_login

            # Update user info if needed
            if is_new_user:
                user.username = user.email.split('@')[0]  # Set username as part of email
                user.save()

            # Generate Django authentication token
            token, _ = Token.objects.get_or_create(user=user)

            return Response({
                'isExistingMember': not is_new_user,
                'token': token.key,
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Login failed'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)





