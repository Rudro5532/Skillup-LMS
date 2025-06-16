from django.shortcuts import render, get_object_or_404,redirect
from .models import Course, Category
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def courses(request):
    search = request.GET.get("search")
    all_course = Course.objects.all().order_by("-created_at")

    context = {
        "courses": all_course,
        "search": search,
    }

    if search:
        search_course = Course.objects.filter(
            Q(name__icontains=search) | Q(description__icontains=search) | Q(category__category_name__icontains=search)
        )
        context["search_course"] = search_course 

    return render(request, "courses/courses.html", context)


@login_required(login_url="user_login")
def get_course(request, slug):
    course = get_object_or_404(Course, slug=slug)
    return render(request, "courses/single_course.html",{"course" : course})