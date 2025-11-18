from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView,
    toggle_favorite_view,
    favorites_list_view,
    HomeView,
    article_comments_api,
    article_comments_count_api,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('articles/', ArticleListView.as_view(), name='article-list'),
    path('article/<slug:slug>/', ArticleDetailView.as_view(), name='article-detail'),
    path('favorites/', favorites_list_view, name='favorites_list'),
    path('favorite/toggle/<int:article_id>/',
         toggle_favorite_view, name='toggle_favorite'),

    # Comment API endpoints
    path('api/articles/<int:article_id>/comments/',
         article_comments_api, name='article-comments-api'),
    path('api/articles/<int:article_id>/comments/count/',
         article_comments_count_api, name='article-comments-count-api'),
]
