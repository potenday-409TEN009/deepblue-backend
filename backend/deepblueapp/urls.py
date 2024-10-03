
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

PostRouter = DefaultRouter()
PostRouter.register(r'posts', views.PostViewSet)
urlpatterns = [
    path('ranking/',views.UserRankingListView.as_view(),name='ranking'),
    path('', include(PostRouter.urls)),
    path('quests/', views.MyQuestListAPIView.as_view(), name='quest_list'),
    path('quests/', views.my_quest_create, name='quest_create'),
    path('quests/{difficulty}', views.MyQuestDoneAPIView.as_view(), name='quest_done'),
    path('dashboard/', views.DashboardAPIView.as_view(), name='dashboard'),
    path('userinfo/', views.UserInfoAPIView.as_view(), name='user_info'),
]

