from django.urls import path, include


urlpatterns = [
    path('api/', include('user_files.api.urls')),
]
