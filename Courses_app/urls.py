from django.urls import path
from . import views


urlpatterns = [
    path("all-courses/", views.courses, name="courses"),
    path("get_single_course/<slug:slug>/", views.get_course, name="get_course")
]
