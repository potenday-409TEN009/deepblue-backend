from rest_framework import serializers
from django.utils import timezone
from .models import UserProfile,Post

class DashboardSerializer(serializers.Serializer):
    cleared_quest_count = serializers.IntegerField()
    total_cleared_day = serializers.IntegerField()
    level = serializers.IntegerField()
    avg_week_cleared_quest = serializers.FloatField()
    daily_check_count = serializers.IntegerField()

class UserRankingSerializer(serializers.Serializer):
    nickname = serializers.CharField()
    score = serializers.IntegerField()
    level = serializers.IntegerField()
    ranking = serializers.IntegerField()
    top_percent = serializers.SerializerMethodField()

    def get_top_percent(self, obj):
        request = self.context.get('request')
        if request and request.user == obj.user:
            total_users = UserProfile.objects.count()
            top_percent = round(100 / total_users * obj.ranking, 2)
            return top_percent
        return None


class PostSerializer(serializers.ModelSerializer):
    nickname = serializers.ReadOnlyField(source='user_profile.nickname')
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return self.get_time_difference(obj.created_at)

    def get_updated_at(self, obj):
        return self.get_time_difference(obj.updated_at)

    def get_time_difference(self, date):
        now = timezone.now()
        diff = now - date

        if diff.days > 1:
            return date.strftime("%m월 %d일")
        elif diff.seconds >= 3600:
            return f"{diff.seconds // 3600}시간 전"
        else:
            return f"{diff.seconds // 60}분 전"
    category = serializers.ChoiceField(choices=['a', 'b', 'c'])
    
    def validate_category(self, value):
        if value not in ['a', 'b', 'c']:
            raise serializers.ValidationError(" a,b,c카테고리만 보내주세요.")
        return value
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['title', 'content', 'created_at', 'updated_at', 'category', 'nickname', 'comment_count','likes']

    def get_comment_count(self, obj):
        return obj.comments.count()
    
class QuestSerializer(serializers.Serializer):
    difficulty = serializers.CharField()
    content = serializers.CharField()
    score = serializers.IntegerField()
    is_cleared = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

