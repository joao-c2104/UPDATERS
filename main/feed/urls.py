from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView,
    toggle_save_article_view,
    saved_articles_list_view,
    HomeView,
    article_comments_api,
    article_comments_count_api,
    FlashVideoListView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('articles/', ArticleListView.as_view(), name='article-list'),
    path('article/<slug:slug>/', ArticleDetailView.as_view(), name='article-detail'),
    path('saved-articles/', saved_articles_list_view, name='saved_articles_list'),
    path('saved/toggle/<int:article_id>/', toggle_save_article_view, name='toggle_save_article'),

    path('favorites/', favorites_list_view, name='favorites_list'),
    path('favorite/toggle/<int:article_id>/', toggle_favorite_view, name='toggle_favorite'),

    path('videos-flash/', FlashVideoListView.as_view(), name='flash_videos'),

    path('api/articles/<int:article_id>/comments/', article_comments_api, name='article-comments-api'),
    path('api/articles/<int:article_id>/comments/count/', article_comments_count_api, name='article-comments-count-api'),
]
