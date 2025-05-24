from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.student_signup, name="signup"),
    path("login/", views.login, name="login"),


    #secure url
    path("teacher_signup/", views.teacher_signup, name="teacher_signup"),
]

