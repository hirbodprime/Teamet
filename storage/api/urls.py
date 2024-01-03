from django.urls import path

from . import views as custom_views


urlpatterns = [
    path('folder/create/', custom_views.FolderCreateAPIView.as_view(), name='folder_create'),
    path('folder/list/', custom_views.FolderListAPIView.as_view(), name='folder_list'),
    path('folder/get/<int:pk>/', custom_views.FolderDetailAPIView.as_view(), name='folder_detail'),
    path('folder/rename/<int:pk>/', custom_views.FolderRenameAPIView.as_view(), name='folder_rename'),
    path('folder/delete/<int:pk>/', custom_views.FolderDeleteAPIView.as_view(), name='folder_delete'),
]
