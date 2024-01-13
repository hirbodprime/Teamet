import os, shutil

from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import FileModel
from .utils import get_path


@receiver(post_save, sender=FileModel)
def set_path(sender, created, instance, **kwargs):
    if created:
        instance.path = get_path(instance.parent_folder, instance.file_field, instance.user_profile.user)
        instance.save()
        