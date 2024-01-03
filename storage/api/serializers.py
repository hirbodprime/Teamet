from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from storage.models import FolderModel
from storage.utils import slugify


class FolderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FolderModel
        fields = ['name', 'user']
        read_only_fields = ['user']

    def validate_name(self, value):
        try:
            user = self.context['request'].user
            FolderModel.objects.get(slug=slugify(value), user=user)
            raise serializers.ValidationError('folder with this name already exists.')
        
        except ObjectDoesNotExist:
            return value

    def create(self, validated_data):
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
        return f'{settings.SITE_DOMAIN}/folders/{obj.user.email}/{obj.slug}'
    

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
    