from django.urls import path
from .views import (
    ArticleListView, 
    ArticleDetailView,
    toggle_favorite_view,
    favorites_list_view,
)

urlpatterns = [
    path('', ArticleListView.as_view(), name='article-list'),
    path('article/<slug:slug>/', ArticleDetailView.as_view(), name='article-detail'),
    path('favorites/', favorites_list_view, name='favorites_list'),
    path('favorite/toggle/<int:article_id>/', toggle_favorite_view, name='toggle_favorite'),
]
