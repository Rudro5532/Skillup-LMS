from django.shortcuts import render
from Courses_app.models import Course

def home(request):
    courses = Course.objects.order_by("created_at")[:3]
    context = {
        'courses' : courses
    }
    return render(request, "home/index.html",context)