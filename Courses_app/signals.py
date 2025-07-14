import os
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Course,CourseVideo

@receiver(pre_save, sender=Course)
def auto_delete_file_on_change(sender,instance,**kwargs):
    if not instance.pk:
        return
    
    try:
        old_course = Course.objects.get(pk=instance.pk)
    except Course.DoesNotExist:
        return
    
    if old_course.image and instance.image and old_course.image != instance.image:
        if os.path.isfile(old_course.image.path):
            os.remove(old_course.image.path)

    if old_course.course_meterial and instance.course_meterial and old_course.course_meterial != instance.course_meterial:
        if os.path.isfile(old_course.course_meterial.path):
            os.remove(old_course.course_meterial.path)


@receiver(pre_save, sender=CourseVideo)
def auto_delete_video_on_change(sender,instance,**kwargs):
    if not instance.pk:
        return
    
    try:
        old_video = CourseVideo.objects.get(pk=instance.pk)
    except CourseVideo.DoesNotExist:
        return
    
    if old_video.video and instance.video and old_video.video != instance.video:
        if os.path.isfile(old_video.video.path):
            os.remove(old_video.video.path) 


