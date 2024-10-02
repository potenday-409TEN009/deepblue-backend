from django.urls import path
from . import views

urlpatterns = [
    path('quests/', views.MyQuestListAPIView.as_view(), name='quest_list'),
    path('quests/', views.my_quest_create, name='quest_create'),
    path('quests/{difficulty}', views.MyQuestDoneAPIView.as_view(), name='quest_done'),
]
