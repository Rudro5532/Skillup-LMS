from django.shortcuts import render, get_object_or_404,redirect
from .models import Course, Category
from django.contrib.auth.decorators import login_required




def courses(request):
    all_course = Course.objects.all().order_by("-created_at")

    context = {
        "courses" : all_course
    }
    return render(request, "courses/courses.html", context)

@login_required(login_url="user_login")
def get_course(request, slug):
    course = get_object_or_404(Course, slug=slug)
    return render(request, "courses/single_course.html",{"course" : course})