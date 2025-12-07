from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView,
    toggle_favorite_view,
    toggle_favorite_redirect_to_saved,
    toggle_favorite_api,
    favorites_list_view,
    saved_articles,
    toggle_save_article,
    HomeView,
    article_comments_api,
    article_comments_count_api,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('articles/', ArticleListView.as_view(), name='article-list'),
    path('article/<slug:slug>/', ArticleDetailView.as_view(), name='article-detail'),

    # Saved articles page (new slug-based implementation)
    path('salvos/', saved_articles, name='saved_articles'),
    path('article/<slug:slug>/toggle-save/',
         toggle_save_article, name='toggle_save_article'),

    # Legacy favorites routes (keeping for backward compatibility)
    path('favorites/', favorites_list_view, name='favorites_list'),
    path('favorite/toggle/<int:article_id>/',
         toggle_favorite_view, name='toggle_favorite'),

    # Toggle favorite and redirect to saved page (for article detail)
    path('favorite/toggle-redirect/<int:article_id>/',
         toggle_favorite_redirect_to_saved, name='toggle_favorite_redirect'),

    # Favorites API endpoint (for AJAX on feed)
    path('api/favorite/toggle/<int:article_id>/',
         toggle_favorite_api, name='toggle-favorite-api'),

    # Comment API endpoints
    path('api/articles/<int:article_id>/comments/',
         article_comments_api, name='article-comments-api'),
    path('api/articles/<int:article_id>/comments/count/',
         article_comments_count_api, name='article-comments-count-api'),
]
