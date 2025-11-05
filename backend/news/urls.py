from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, CommentViewSet, VideoViewSet, PollViewSet

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'videos', VideoViewSet)
router.register(r'polls', PollViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
