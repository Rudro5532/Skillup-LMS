import os
from django.db.models.signals import pre_save 
from django.dispatch import receiver
from .models import User

@receiver(pre_save, sender=User)
def auto_delete_profileImage_onchange(sender,instance,**kwargs):
    if not instance.pk:
        return
    try:
        old_image = User.objects.get(pk=instance.pk)
    except User.DoesNotExist:
        return
    
    if old_image.profile_image and instance.profile_image and old_image.profile_image != instance.profile_image:
        if os.path.isfile(old_image.profile_image.path):
            os.remove(old_image.profile_image.path)