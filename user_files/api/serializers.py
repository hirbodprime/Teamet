from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from user.models import ProfileModel
from user_files.models import FileModel
from user_files.utils import get_depth


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileModel
        fields = ['id', 'file_field', 'path', 'parent_folder', 'user_profile']
        read_only_fields = ['id', 'user_profile', 'path']
        extra_kwargs = {'file_field': {'write_only': True},}
    
    def validate_parent_folder(self, value):
        if value.user_profile.user == self.context['request'].user:
            return value
        raise serializers.ValidationError('this folder does not exists for this user.')
    
    def validate(self, attrs):
        user = self.context['request'].user
        file_field = attrs['file_field']
        try:
            user_profile = ProfileModel.objects.get(user=user)
            attrs['user_profile'] = user_profile
        except ObjectDoesNotExist:
            raise serializers.ValidationError('internal error: this user does not have a profile')
        
        if user_profile.used_storage + file_field.size > settings.USER_STORAGE_LIMIT:
            raise serializers.ValidationError('you do not have enough storage to upload this file.')
        return attrs

    def create(self, validated_data):
        parent = validated_data.get('parent_folder')
        file_field = validated_data['file_field']
        user_profile = validated_data['user_profile']
        depth = get_depth(parent, file_field, user_profile.user)
        validated_data['depth'] = depth
        return super().create(validated_data)
    

class FileListDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user_profile.user.email')
    path = serializers.SerializerMethodField()

    class Meta:
        model = FileModel
        fields = ['id', 'user', 'depth', 'parent_folder', 'path']

    def get_path(self, obj):
        return f'{settings.MEDIA_URL}{obj.path}'
    