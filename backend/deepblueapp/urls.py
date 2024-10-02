
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet


PostRouter = DefaultRouter()
PostRouter.register(r'posts', PostViewSet)
urlpatterns = [
    path('', include(PostRouter.urls)),
]
