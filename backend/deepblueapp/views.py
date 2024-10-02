from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from .models import Quest, QuestList
from .serializers import QuestSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view

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
