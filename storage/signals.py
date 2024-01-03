import os

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


User = get_user_model()


@receiver(post_save, sender=User)
def create_folder(sender, created, instance, **kwargs):
    if created:
        try:
            os.mkdir(f'./folders/{instance.email}')
        
        except Exception as e:
            print(e)
            