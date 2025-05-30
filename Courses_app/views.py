from django.shortcuts import render
from .models import Course


def courses(request):
    all_course = Course.objects.all().order_by("-created_at")

    context = {
        "courses" : all_course
    }
    return render(request, "courses/courses.html", context)