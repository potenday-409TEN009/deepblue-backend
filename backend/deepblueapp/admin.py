from django.contrib import admin
from .models import UserProfile, Post,Comment, Quest, DailyCheck, QuestList


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    pass

@admin.register(DailyCheck)
class DailyCheckAdmin(admin.ModelAdmin):
    pass

@admin.register(QuestList)
class QuestListAdmin(admin.ModelAdmin):
    pass

