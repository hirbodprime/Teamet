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
from storage.utils import slugify
from storage.models import FolderModel
from storage.permissions import IsOwnerOrAdmin


class FolderCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = custom_serializers.FolderCreateRenameSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            folder_name = serializer.validated_data.get('name')
            os.mkdir(f'./folders/{request.user.email}/{slugify(folder_name)}')
            self.perform_create(serializer)
            response_data = {'message': 'folder created.'}
            status_code = status.HTTP_201_CREATED

        except FileExistsError:
            status_code = status.HTTP_400_BAD_REQUEST
            response_data = {'error': 'folder with this name already exists.'}

        except Exception as e:
            print(str(e))
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            response_data = {'error': 'folder creation failed.'}

        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status_code, headers=headers)

    
class FolderListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = custom_serializers.FolderListDetailSerializer
    
    def get_queryset(self):
        return FolderModel.objects.filter(user=self.request.user)


class FolderDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = custom_serializers.FolderListDetailSerializer
    
    def get_object(self):
        folder_id = self.kwargs.get('pk')
        return get_object_or_404(FolderModel, pk=folder_id)
    

class FolderRenameAPIView(generics.UpdateAPIView):
    permission_classes = [IsOwnerOrAdmin]
    queryset = FolderModel.objects.all()
    serializer_class = custom_serializers.FolderCreateRenameSerializer

    def perform_update(self, serializer):
        try:
            folder = self.get_object()
            folder_path = f'./folders/{folder.user.email}/{folder.slug}'
            new_path = f'./folders/{folder.user.email}/{serializer.validated_data.get("name")}'
            # development
            # folder_path = f'{settings.SITE_DOMAIN}/folders/{folder.user.email}/{folder.slug}'
            # new_path = f'{settings.SITE_DOMAIN}/folders/{folder.user.email}/{serializer.validated_data.get("name")}'
            os.rename(folder_path, new_path)

        except Exception as e:
            print(str(e))
            raise APIException({'error': 'operation failed.'}, code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        serializer.save()


class FolderDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [IsOwnerOrAdmin]
    queryset = FolderModel

    def perform_destroy(self, instance):
        try:
            folder_path = f'./folders/{instance.user.email}/{instance.slug}'
            # development
            # folder_path = f'{settings.SITE_DOMAIN}/folders/{instance.user.email}/{instance.slug}'
            shutil.rmtree(folder_path)
            instance.delete()
        
        except Exception as e:
            print(str(e))
            raise APIException({'error': 'operation failed.'}, code=status.HTTP_500_INTERNAL_SERVER_ERROR)
