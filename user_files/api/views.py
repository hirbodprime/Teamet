import os, shutil

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from rest_framework import generics, views
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import serializers as custom_serializers
from storage.permissions import IsOwnerOrAdmin
from user_files.models import FileModel


class FileUploadAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = custom_serializers.FileUploadSerializer

    def perform_create(self, serializer):
        serializer.save()
        file_field = serializer.validated_data['file_field']
        user_profile = serializer.validated_data['user_profile']
        user_profile.used_storage += file_field.size
        user_profile.save()
    

class FileListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = custom_serializers.FileListDetailSerializer
    
    def get_queryset(self):
        return FileModel.objects.filter(user_profile__user=self.request.user)
    

class FileDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = custom_serializers.FileListDetailSerializer
    queryset = FileModel.objects.all()
    

class FileDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [IsOwnerOrAdmin]
    queryset = FileModel.objects.all()

    def perform_destroy(self, instance):
        try:
            file_size = instance.file_field.size
            file_path = f'{settings.MEDIA_ROOT}/{instance.path}'
            os.remove(file_path)
            instance.user_profile.used_storage -= file_size
            instance.user_profile.save()
            instance.delete()
        
        except Exception as e:
            print(str(e))
            raise APIException({'error': 'operation failed.'}, code=status.HTTP_500_INTERNAL_SERVER_ERROR)
