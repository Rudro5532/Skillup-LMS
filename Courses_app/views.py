from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
from .models import Course, Category,CourseReview,CourseVideo
from Payment_app.models import Payment
from Account_app.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse


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
    if request.method == "POST":
        comment = request.POST.get("comment")
        if comment:
            comment = CourseReview.objects.create(
                course = course,
                user = request.user,
                comment = comment
            )
            comment.save()
            return JsonResponse({
                "success" : True,
                "message" : "Thanks for review",
                "redirect_url" : reverse("get_course", kwargs={"slug": course.slug})
            })
    enrollment = Payment.objects.filter(user=request.user, course=course, is_paid = True).exists()
    review = CourseReview.objects.filter(course=course).order_by("-created_at")
    videos = CourseVideo.objects.filter(course=course)
    context = {
        "course" : course,
        "enrollment" : enrollment,
        "review" : review,
        "videos" : videos
    }

    return render(request, "courses/single_course.html", context)

