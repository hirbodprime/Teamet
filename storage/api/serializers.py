from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers, status

from storage.models import FolderModel
from storage.utils import slugify, get_path_depth, check_depth
from user.models import ProfileModel
from user_files.api.serializers import FileListDetailSerializer


class FolderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FolderModel
        fields = ['name', 'path', 'depth', 'parent_folder', 'user_profile']
        read_only_fields = ['user_profile', 'path']

    def validate_parent_folder(self, value):
        if value.user_profile.user == self.context['request'].user:
            return value
        raise serializers.ValidationError('this folder does not exists for this user.')

    def validate(self, attrs):
        name = attrs.get('name')
        parent = attrs.get('parent_folder')
        depth_allowed = check_depth(parent)

        if not depth_allowed:
            raise serializers.ValidationError('maximum depth reached. you cannot create a sub-folder in this folder.')

        try:
            user = self.context['request'].user
            user_profile = ProfileModel.objects.get(user=user)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('internal error: this user does not have a profile.', code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        try:
            FolderModel.objects.get(slug=slugify(name), parent_folder=parent, user_profile=user_profile)
            raise serializers.ValidationError('folder with this name already exists.')
        except ObjectDoesNotExist:
            pass

        return super().validate(attrs)

    def create(self, validated_data):
        # Automatically set the user from the request
        user = self.context['request'].user
        user_profile = ProfileModel.objects.get(user=user)
        validated_data['user_profile'] = user_profile
        name = validated_data.get('name')
        parent = validated_data.get('parent_folder')
        path, depth = get_path_depth(parent, name, user)
        validated_data['path'] = path
        validated_data['depth'] = depth
        return super().create(validated_data)
    

class FolderListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user_profile.user.email')
    path = serializers.SerializerMethodField()

    class Meta:
        model = FolderModel
        fields = ['id', 'user', 'name', 'slug', 'depth', 'parent_folder','created_at', 'path']

    def get_path(self, obj):
        if obj.path:
            return f'{settings.MEDIA_URL}{obj.path}'
        return


class SubFolderListSerializer(serializers.ModelSerializer):
    path = serializers.SerializerMethodField()
    folder_files = FileListDetailSerializer(read_only=True, many=True)

    class Meta:
        model = FolderModel
        fields = ['id', 'name', 'slug', 'depth', 'created_at', 'path', 'folder_files']

    def get_path(self, obj):
        if obj.path:
            return f'{settings.MEDIA_URL}{obj.path}'
        return
    

class FolderDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user_profile.user.email')
    sub_folders = SubFolderListSerializer(many=True, read_only=True)
    path = serializers.SerializerMethodField()

    class Meta:
        model = FolderModel
        fields = ['id', 'user', 'name', 'slug', 'depth', 'parent_folder','created_at', 'path', 'sub_folders']

    def get_path(self, obj):
        if obj.path:
            return f'{settings.MEDIA_URL}{obj.path}'
        return
    

class FolderRenameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FolderModel
        fields = ['name', 'path']
        read_only_fields = ['path']

    def validate_name(self, value):
        try:
            user = self.context['request'].user
            user_profile = ProfileModel.objects.get(user=user)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('internal error: this user does not have a profile.', code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try:
            FolderModel.objects.get(slug=slugify(value), user_profile=user_profile)
            raise serializers.ValidationError('folder with this name already exists.', code=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            return value
        
    def update(self, instance, validated_data):
        name = validated_data.get('name')
        parent = instance.parent_folder
        path, depth = get_path_depth(parent, name, instance.user_profile.user)
        validated_data['path'] = path
        return super().update(instance, validated_data)    
    