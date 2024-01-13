from django.db import models

from storage.utils import slugify
from user.models import ProfileModel



class FolderModel(models.Model):
    class Meta:
        verbose_name = 'Folder'
        verbose_name_plural = 'Folders'

    user_profile = models.ForeignKey(ProfileModel, on_delete=models.CASCADE, related_name='folders')
    # depth: number of parent folders, 0: no parent, 1: one parent
    parent_folder = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='sub_folders')
    depth = models.IntegerField(default=0)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    path = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk}-{self.path}'
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    