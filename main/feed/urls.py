from django.urls import path
from .views import (
    ArticleListView, 
    ArticleDetailView,
    login_user,
    submit_login,
    register_user,
    logout_user
)

urlpatterns = [
    path('', ArticleListView.as_view(), name='article-list'),
    path('article/<slug:slug>/', ArticleDetailView.as_view(), name='article-detail'),
    path('login/', login_user, name='login_user'), 
    path('login/submit/', submit_login, name='submit_login'),
    path('register/', register_user, name='register_user'),
    path('logout/', logout_user, name='logout_user'),
]
