from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')), # Mantivemos essa linha importante do antigo
    path('', include('feed.urls')),
    path('', include('login.urls')),
]

# Configuração para forçar o Django a servir imagens no Render
# Substitui o "if settings.DEBUG" antigo para funcionar sempre
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]