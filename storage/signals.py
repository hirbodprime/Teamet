import os, shutil

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import FolderModel
from user_files.models import FileModel
from user_files.utils import get_new_name


User = get_user_model()


@receiver(post_save, sender=User)
def create_folder(sender, created, instance, **kwargs):
    if created:
        try:
            os.mkdir(f'{settings.MEDIA_ROOT}/{instance.email}')
        
        except Exception as e:
            print(e)
            

@receiver(post_delete, sender=User)
def delete_folder(sender, instance, **kwargs):
    try:
        shutil.rmtree(f'{settings.MEDIA_ROOT}/{instance.email}')

    except Exception as e:
        print(str(e))


@receiver(post_save, sender=FolderModel)
def update_subfolders_files(sender, created, instance, **kwargs):
    if not created:
        sub_folders = FolderModel.objects.filter(parent_folder=instance.id)
        
        for folder in sub_folders:
            folder.path = f'{instance.slug}/{folder.slug}'
            folder.save()
        
        objects = FileModel.objects.filter(parent_folder=instance.id)
        for obj in objects:
            obj.path = f'{obj.parent_folder.path}/{obj.path.split("/")[-1]}'
            obj.save()


@receiver(post_delete, sender=FolderModel)
def delete_folder(sender, instance, **kwargs):
    try:
        folder_path = f'{settings.MEDIA_ROOT}/{instance.path}'
        shutil.rmtree(folder_path)
    
    except Exception as e:
        print(str(e))
