from django.urls import path
from .views import ArticleListView, ArticleDetailView
from . import views

urlpatterns = [
    path('', ArticleListView.as_view(), name='article-list'),
    path('article/<slug:slug>/', ArticleDetailView.as_view(), name='article-detail'),
    path('login/', views.login_user, name='login_user'),
    path('login/submit/', views.submit_login, name='submit_login'),
    path('logout/', views.logout_user, name='logout_user'),
    path('register/',views.register_user,name='register_user'),
]
