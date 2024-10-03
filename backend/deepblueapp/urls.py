from .views import UserRankingListView,UserRankingPercentView
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet

PostRouter = DefaultRouter()
PostRouter.register(r'posts', PostViewSet)
urlpatterns = [
    path('ranking/',UserRankingListView.as_view(),name='ranking'),
    path('', include(PostRouter.urls)),
]





