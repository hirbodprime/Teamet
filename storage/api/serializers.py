from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from storage.models import FolderModel
from storage.utils import slugify, generate_path


class FolderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FolderModel
        fields = ['name', 'parent_folder', 'user']
        read_only_fields = ['user']

    def validate(self, attrs):
        name = attrs.get('name')
        parent = attrs.get('parent_folder')

        try:
            user = self.context['request'].user
            FolderModel.objects.get(slug=slugify(name), parent_folder=parent, user=user)
            raise serializers.ValidationError('folder with this name already exists.')
        
        except ObjectDoesNotExist:
            pass

        return super().validate(attrs)

    def create(self, validated_data):
        name = validated_data.get('name')
        parent = validated_data.get('parent_folder')
        validated_data['path'] = generate_path(parent, name)
        # Automatically set the user from the request
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    

class FolderListDetailSerializer(serializers.ModelSerializer):
    path = serializers.SerializerMethodField(read_only=True)
    user = serializers.CharField(source='user.email')

    class Meta:
        model = FolderModel
        fields = ['id', 'user', 'name', 'slug', 'created_at', 'path']

    def get_path(self, obj):
        return f'{settings.FOLDER_ROOT}/{obj.user.email}/{obj.path}'
    

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
    