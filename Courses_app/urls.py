from django.urls import path
from . import views


urlpatterns = [
    path("all-courses", views.courses, name="courses")
]
