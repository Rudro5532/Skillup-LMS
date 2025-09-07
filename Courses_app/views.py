from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
from .models import Course, Category,CourseReview,CourseVideo
from Payment_app.models import Payment
from Account_app.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
# Configure once
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load model once
model = genai.GenerativeModel("gemini-1.5-flash")

def courses(request):
    search = request.GET.get("search")
    all_course = Course.objects.all().order_by("-created_at")

    context = {
        "courses": all_course,
        "search": search,
    }

    if search:
        all_courses = Course.objects.all().values("name", "description", "price", "slug")
        if all_courses:
            course_list_text = "\n".join(
                [f"- {c['name']} (₹{c['price']}) : {c['description']}" for c in all_courses]
            )

            prompt = f"""
            You are an AI course recommender.
            User searched for: "{search}"

            Available courses in the LMS:
            {course_list_text}

            From ONLY these courses, suggest the top 5 most relevant ones.
            Respond with exactly this format:
              1. Course Title
              2. ...
            """

            response = model.generate_content(prompt)

            search_course = []
            if response.text:
                lines = [line.strip() for line in response.text.split("\n") if line.strip()]
                for line in lines:
                    if line[0].isdigit():
                        title = line.lstrip("1234567890. ").strip()
                        course_obj = Course.objects.filter(name__icontains=title).first()
                        if course_obj:
                            search_course.append(course_obj)

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

