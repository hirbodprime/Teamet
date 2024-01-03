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
from storage.utils import get_path_depth
from storage.models import FolderModel
from storage.permissions import IsOwnerOrAdmin


class FolderCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = custom_serializers.FolderCreateSerializer

    def perform_create(self, serializer):
        serializer.save()
        path = serializer.data.get('path')

        try:
            os.mkdir(f'./{settings.FOLDER_ROOT}/{self.request.user.email}/{path}')
            response_data = {'message': 'folder created.'}
            status_code = status.HTTP_201_CREATED

        except FileExistsError:
            status_code = status.HTTP_400_BAD_REQUEST
            response_data = {'error': 'folder with this name already exists.'}

        except Exception as e:
            print(str(e))
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            response_data = {'error': 'folder creation failed.'}

        return Response(response_data, status=status_code)

    
class FolderListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = custom_serializers.FolderListSerializer
    
    def get_queryset(self):
        return FolderModel.objects.filter(user=self.request.user)


class FolderDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = custom_serializers.FolderDetailSerializer
    queryset = FolderModel.objects.all()
    

class FolderRenameAPIView(generics.UpdateAPIView):
    permission_classes = [IsOwnerOrAdmin]
    queryset = FolderModel.objects.all()
    serializer_class = custom_serializers.FolderRenameSerializer

    def perform_update(self, serializer):
        
        try:
            folder = self.get_object()
            new_name = serializer.validated_data.get('name')
            parent = self.get_object().parent_folder
            new_path, depth = get_path_depth(parent, new_name)
            old_path = f'./{settings.FOLDER_ROOT}/{folder.user.email}/{folder.path}'
            new_path = f'./{settings.FOLDER_ROOT}/{folder.user.email}/{new_path}'
            os.rename(old_path, new_path)
            serializer.save()

        except Exception as e:
            print(str(e))
            raise APIException({'error': 'operation failed.'}, code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class FolderDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [IsOwnerOrAdmin]
    queryset = FolderModel

    def perform_destroy(self, instance):
        try:
            folder_path = f'./folders/{instance.user.email}/{instance.slug}'
            shutil.rmtree(folder_path)
            instance.delete()
        
        except Exception as e:
            print(str(e))
            raise APIException({'error': 'operation failed.'}, code=status.HTTP_500_INTERNAL_SERVER_ERROR)
