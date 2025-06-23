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
    course_meterial = models.FileField(upload_to="course_meterial/")
    price = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[('Enrolled', 'Enrolled'), ('Pending', 'Pending')],
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True) 

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"
    

class CourseReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return f"{self.user} - {self.course}"



