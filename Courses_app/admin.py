from django.contrib import admin
from .models import Category, Course

class CourseAdmin(admin.ModelAdmin):
    list_display = ["name", "image", "category"]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["category_name"]



admin.site.register(Category, CategoryAdmin)
admin.site.register(Course,CourseAdmin)
