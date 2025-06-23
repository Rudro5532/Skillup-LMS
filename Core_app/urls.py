from django.urls import path
from . import views

urlpatterns = [
    path("about_us/", views.about, name="about"),
    path("contact_us/", views.contact, name="contact")
    
]
