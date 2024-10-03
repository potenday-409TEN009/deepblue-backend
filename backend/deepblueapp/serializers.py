from rest_framework import serializers

from .models import UserProfile

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