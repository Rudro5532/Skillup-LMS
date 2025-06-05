from django.urls import path
from . import views

urlpatterns = [
    path("signup/student/", views.signup, name="signup"),
    #secure url
    path("signup/teacher/", views.signup, name="teacher_signup"),
    path('activate/<uidb64>/<token>/', views.activation_view, name='activate'),
    path("user_login/", views.user_login, name="user_login"),
    path("user_logout/", views.user_logout, name="user_logout"),
    path("student_dashboard/", views.student_dashboard, name="student_dashboard"),
    path("teacher_dashboard/", views.teacher_dashboard, name="teacher_dashboard"),


    
]

