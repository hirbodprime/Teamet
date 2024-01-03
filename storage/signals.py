import os

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import FolderModel
from .utils import get_path_depth


User = get_user_model()


@receiver(post_save, sender=User)
def create_folder(sender, created, instance, **kwargs):
    if created:
        try:
            os.mkdir(f'./folders/{instance.email}')
        
        except Exception as e:
            print(e)
            
            
@receiver(post_save, sender=FolderModel)
def update_subfolders(sender, created, instance, **kwargs):
    if not created:
        sub_folders = FolderModel.objects.filter(parent_folder=instance.id)

        for folder in sub_folders:
            folder.path = f'{instance.slug}/{folder.slug}'
            folder.save()
            