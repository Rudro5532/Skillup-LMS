from django.db import models
from django.utils import timezone
from Account_app.models import User

class Category(models.Model):
    category_name = models.CharField(max_length=100)


    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name
    

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_teacher':True})
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="courses")
    slug = models.SlugField(unique=True, null=True, default="")
    image = models.ImageField(upload_to="course_image/")
    price = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    

