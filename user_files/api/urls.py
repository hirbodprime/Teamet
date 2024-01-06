from django.urls import path

from . import views as custom_views


urlpatterns = [
    path('upload/', custom_views.FileUploadAPIView.as_view(), name='file-upload'),
    path('list/', custom_views.FileListAPIView.as_view(), name='file-list'),
    path('get/<int:pk>/', custom_views.FileDetailAPIView.as_view(), name='file-detail'),
    path('delete/<int:pk>/', custom_views.FileDeleteAPIView.as_view(), name='file-delete'),
]
