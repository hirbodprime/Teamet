from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from storage.models import FolderModel
from storage.utils import slugify, get_path_depth, check_depth


class FolderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FolderModel
        fields = ['name', 'path', 'depth', 'parent_folder', 'user']
        read_only_fields = ['user', 'path']

    def validate_parent_folder(self, value):
        if value.user == self.context["request"].user:
            return value
        
        raise serializers.ValidationError('this folder does not exists for this user.')

    def validate(self, attrs):
        name = attrs.get('name')
        parent = attrs.get('parent_folder')
        depth_allowed = check_depth(parent)

        if not depth_allowed:
            raise serializers.ValidationError('you cannot create a sub-folder in this folder.')

        try:
            user = self.context['request'].user
            FolderModel.objects.get(slug=slugify(name), parent_folder=parent, user=user)
        
        except ObjectDoesNotExist:
            pass

        return super().validate(attrs)

    def create(self, validated_data):
        name = validated_data.get('name')
        parent = validated_data.get('parent_folder')
        path, depth = get_path_depth(parent, name)
        validated_data['path'] = path
        validated_data['depth'] = depth
        # Automatically set the user from the request
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    

class FolderListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.email')

    class Meta:
        model = FolderModel
        fields = ['id', 'user', 'name', 'slug', 'created_at', 'path']


class SubFolderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FolderModel
        fields = ['id', 'user', 'name', 'slug', 'created_at', 'path']
    

class FolderDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.email')
    sub_folders = SubFolderListSerializer(many=True, read_only=True)

    class Meta:
        model = FolderModel
        fields = ['id', 'user', 'name', 'slug', 'created_at', 'path', 'sub_folders']


class FolderRenameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FolderModel
        fields = ['name']

    def validate_name(self, value):
        try:
            user = self.context['request'].user
            FolderModel.objects.get(slug=slugify(value), user=user)
            raise serializers.ValidationError('folder with this name already exists.')
        
        except ObjectDoesNotExist:
            return value
        
    def update(self, instance, validated_data):
        name = validated_data.get('name')
        parent = validated_data.get('parent_folder')
        path, depth = get_path_depth(parent, name)
        validated_data['path'] = path
        return super().update(instance, validated_data)    
    