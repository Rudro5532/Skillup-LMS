from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.student_signup, name="signup"),
    path("user_login/", views.user_login, name="user_login"),
    path("user_logout/", views.user_logout, name="user_logout"),
    path("student_dashboard/", views.student_dashboard, name="student_dashboard"),
    path("teacher_dashboard/", views.teacher_dashboard, name="teacher_dashboard"),


    #secure url
    path("teacher_signup/", views.teacher_signup, name="teacher_signup"),
]

