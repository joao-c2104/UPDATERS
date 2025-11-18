from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('feed.urls')),
    path('', include('login.urls')),
]

if settings.DEBUG:
    # MÍDIA: Serve arquivos de mídia enviados por usuários em desenvolvimento
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # NOTA: Static files são servidos automaticamente pelo Django em DEBUG=True
    # através do django.contrib.staticfiles app