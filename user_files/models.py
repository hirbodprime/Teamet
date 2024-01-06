from django.contrib.auth import get_user_model
from django.db import models

from storage.models import FolderModel
from .utils import get_path


User = get_user_model()


def upload_path(instance, filename):
    if instance.parent_folder:
        return f'{instance.parent_folder.path}/{filename}'
    return f'{instance.user.email}/{filename}'


class FileModel(models.Model):
    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_files')
    parent_folder = models.ForeignKey(FolderModel, on_delete=models.CASCADE, blank=True, null=True, related_name='folder_files')
    path = models.TextField()
    # depth: number of parent folders, 0: no parent, 1: one parents, 2: two parents
    depth = models.IntegerField(default=0)
    file_field = models.FileField(upload_to=upload_path)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk}-{self.path}'
    
        