from django.urls import path
from . import views

urlpatterns = [
    path("course_payment/", views.course_enrolled, name="course_payment"),
    path("verify_payment/", views.verify_payment, name="verify_payment")
]
