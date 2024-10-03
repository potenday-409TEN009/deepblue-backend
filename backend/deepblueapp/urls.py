from django.urls import path
from .views import UserRankingListView,UserRankingPercentView

urlpatterns = [
    path('ranking/',UserRankingListView.as_view(),name='ranking'),
]
