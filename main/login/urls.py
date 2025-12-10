from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login_user'), 
    path('register/', views.register_user, name='register_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('recuperar-senha/', views.forgot_password, name='forgot_password'),
    path('recuperar-senha/enviar/', views.submit_forgot_password, name='submit_forgot_password'),
]