from django.urls import path
from . import views

urlpatterns = [
    path("signup/student/", views.signup, name="signup"),
    #secure url
    path("signup/teacher/", views.signup, name="teacher_signup"),
    path("signup/lms_admin/", views.admin_reg, name="admin_reg"),
    path('activate/<uidb64>/<token>/', views.activation_view, name='activate'),
    path("user_login/", views.user_login, name="user_login"),
    path("user_logout/", views.user_logout, name="user_logout"),
    path("student_dashboard/", views.student_dashboard, name="student_dashboard"),
    path('students/', views.enrolled_students_list, name='enrolled_students'),
    path("teacher_dashboard/", views.teacher_dashboard, name="teacher_dashboard"),
    path("course_video/",views.course_video,name="course_video"),
    path("edit_video/<int:id>/", views.edit_course_video, name="edit_course_video"),
    path("delete_video/<int:id>/", views.delete_course_video, name="delete_course_video"),
    path("update_course/<slug:slug>/", views.edit_course, name="update_course"),
    path("delete_course/<slug:slug>/", views.delete_course, name="delete"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("change_password/", views.change_password, name="change_password"),
    path("forgot_password/", views.send_otp_view, name="forgot_password"),
    path("reset_password/", views.reset_password, name="reset_password")
]

