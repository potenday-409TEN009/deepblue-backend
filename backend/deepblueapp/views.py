from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta

from .serializers import DashBoardSerializer
from .models import DailyCheck, Quest

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


        