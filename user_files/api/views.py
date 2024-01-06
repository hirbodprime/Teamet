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
    

class FileListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = custom_serializers.FileListDetailSerializer
    
    def get_queryset(self):
        return FileModel.objects.filter(user=self.request.user)
    

class FileDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = custom_serializers.FileListDetailSerializer
    queryset = FileModel.objects.all()
    

class FileDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [IsOwnerOrAdmin]
    # serializer_class = custom_serializers.FileListDetailSerializer
    queryset = FileModel.objects.all()