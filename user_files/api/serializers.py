from django.conf import settings

from rest_framework import serializers

from user.models import ProfileModel
from user_files.models import FileModel
from user_files.utils import get_depth


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileModel
        fields = ['file_field', 'path', 'parent_folder', 'user_profile']
        read_only_fields = ['user_profile', 'path']
        extra_kwargs = {'file_field': {'write_only': True},}

    def validate_parent_folder(self, value):
        if value.user_profile.user == self.context['request'].user:
            return value
        raise serializers.ValidationError('this folder does not exists for this user.')

    def create(self, validated_data):
        user = self.context['request'].user
        user_profile = ProfileModel.objects.get(user=user)
        validated_data['user_profile'] = user_profile
        parent = validated_data.get('parent_folder')
        file_field = validated_data['file_field']
        depth = get_depth(parent, file_field, user)
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
    