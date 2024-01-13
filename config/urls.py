from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('storage/', include('storage.urls')),
    path('files/', include('user_files.urls')),
    path('orders/', include('orders.urls')),
    path('openai/', include('openai_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    