from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import User
from Courses_app.models import Category,Course
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .authentication import create_access_token,create_refresh_token
import re
import os
from dotenv import load_dotenv
load_dotenv()



#regex_part
name_regex = r'^([A-Za-z]{2,})(\s[A-Za-z]{2,})+$'
username_regex = r'^@([a-z0-9_]{3,})$'
email_regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
password_regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*_-])[A-Za-z\d!@#$%^&*_-]{6,}'

def signup(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if 'teacher' in request.path:
            is_teacher = True
            is_staff = True
            #show_subject = True
        else:
            is_teacher = False
            #show_subject = False
            is_staff = False

        if request.method == 'POST':
            full_name = request.POST.get("name")
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            subject = request.POST.get("subject") if is_teacher else ''

            if not password == confirm_password:
                return JsonResponse({
                    "message" : "Password and confirm password must be same",
                    "success" : False
                })
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({
                    "message" : "Email already register",
                    "success" : False
                })

            if not re.fullmatch(password_regex, password ):
                return JsonResponse({
                    "message" : "write minimum 6 chracter of password. Minimum one capital letter one small letter one digit and one special charecter.",
                    "success" : False
                })
            
            if not re.fullmatch(name_regex, full_name):
                return JsonResponse({
                    "message" : "Please write your full and correct name",
                    "success" : False
                })

            
            if not re.fullmatch(username_regex,username):
                return JsonResponse({
                    "message" : "Start with @ and use one number and always use small letter",
                    "success" : False
                })
            
            if not re.fullmatch(email_regex, email):
                return JsonResponse({
                    "message" : "Please write correct format of email",
                    "success" : False
                })
            
            user = User(
                full_name = full_name,
                username = username,
                email = email,
                password=password,
                subject = subject,
                is_teacher = is_teacher,
                is_staff = is_staff
            )
            user.set_password(password)
            user.save()
            try:
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                activation_link = f"http://localhost:8000/account/activate/{uidb64}/{token}/"
                subject_line = "Activate your Skillup account"
                message = f"Hi {full_name},\nClick here to activate your account:\n{activation_link}"
                send_mail(subject_line, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)

                return JsonResponse({"message": "Registration successful! Check your email to activate.", "success": True})

            except Exception as e:
                user.delete()
                return JsonResponse({"message": "Email sending failed. Try again.", "success": False})

    return render(request, "account/signup.html")
    

def activation_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(id=uid)
    except:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('user_login')
    else:
        return HttpResponse("Invalid or expired activation link.")



def user_login(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")

            user = authenticate(request, email = email, password = password)

            if user is not None:
                login(request, user)
                access_token = create_access_token(user.id)
                refresh_token = create_refresh_token(user.id)

                print("Access token key:", access_token)
                print("Refresh token key:", refresh_token)

                response = JsonResponse({
                    "success" : True,
                    "message" : "Login successfull !",
                    "access_token" : access_token,
                    "refresh_token" : refresh_token,
                    "redirect_url" : "/account/teacher_dashboard/" if user.is_teacher else "/account/student_dashboard/"
                })

                response.set_cookie(
                    key="refresh_token",
                    value= refresh_token,
                    httponly=True
                )

                response.set_cookie(
                    key="access_token",
                    value= access_token,
                    httponly=True
                )
                return response
            else:
                return JsonResponse({
                    "success" : False,
                    "message" : "Invalid credential !",
                    "redirect_url" : "/account/user_login/"
                })
        return render(request, "account/login.html")

@login_required(login_url="home")
def user_logout(request):
    logout(request)
    return redirect("home")

def is_student(user):
   return user.is_authenticated and not user.is_teacher

@login_required(login_url="user_login")
@user_passes_test(is_student, login_url='teacher_dashboard')
def student_dashboard(request):
    return render(request, "account/student_dashboard.html")

def is_teacher(user):
   return user.is_teacher

@login_required(login_url='user_login')
@user_passes_test(is_teacher, login_url='home')
def teacher_dashboard(request):
    if request.method == "POST":
        name = request.POST.get("title")
        category_id = request.POST.get("category")
        teacher_id = request.POST.get("teacher")
        price = request.POST.get("price")
        description = request.POST.get("description")
        slug = request.POST.get("slug")
        image = request.FILES.get("image")
        course_meterial = request.FILES.get("meterial")
        category = get_object_or_404(Category, id=category_id)
        teacher = get_object_or_404(User, id=teacher_id)

        if not all([name,category_id,teacher_id,price,description,slug,image,course_meterial]):
            return JsonResponse({
                "success" : False,
                "message" : "All fields are required for post the course"
            }) 
        
        create_blog = Course(
            name = name,
            category = category,
            teacher = teacher,
            price = price,
            description = description,
            slug = slug,
            image = image,
            course_meterial = course_meterial
        )
        create_blog.save()
        return JsonResponse({
            "success" : True,
            "message" : "Course published successfully"
        })
        #return redirect("teacher_dashboard")
    categories = Category.objects.all()
    teachers = User.objects.filter(is_teacher=True)
    courses = Course.objects.all()
    students = User.objects.filter(is_teacher=False, is_superuser=False)
    context= {
        'categories' : categories,
        'teachers' : teachers,
        'courses' : courses,
        'students' : students
    }
    return render(request, "account/teacher_dashboard.html", context)
    
@login_required(login_url='user_login')
@user_passes_test(is_teacher, login_url='home')
def edit_course(request, slug):
    course = get_object_or_404(Course, slug=slug) if slug else None
    if request.method == "POST":
        name = request.POST.get("title")
        category_id = request.POST.get("category")
        teacher_id = request.POST.get("teacher")
        price = request.POST.get("price")
        description = request.POST.get("description")
        new_slug = request.POST.get("slug")
        image = request.FILES.get("image")
        course_meterial = request.FILES.get("meterial")

        # Validation check
        if not all([name, category_id, teacher_id, price, description, new_slug]):
            return JsonResponse({
                "success": False,
                "message": "All fields are required for post the course"
            })

        category = get_object_or_404(Category, id=category_id)
        teacher = get_object_or_404(User, id=teacher_id)

        # Slug uniqueness check
        if new_slug != course.slug:
            if Course.objects.filter(slug=new_slug).exclude(id=course.id).exists():
                return JsonResponse({
                    "success": False,
                    "message": "This slug already exists."
                })
            course.slug = new_slug

        # Assign all values
        course.name = name
        course.category = category
        course.teacher = teacher
        course.price = price
        course.description = description
        if image and course_meterial:
            course.image = image
            course.course_meterial = course_meterial

        course.save()
        return JsonResponse({
            "success": True,
            "message": "Course updated successfully"
        })

    teachers = User.objects.filter(is_teacher=True)
    courses = Course.objects.all()
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'teachers': teachers,
        'courses': courses,
        'course_details': course
    }
    return render(request, "account/teacher_dashboard.html", context)

@login_required(login_url='user_login')
@user_passes_test(is_teacher, login_url='home')
def delete_course(request, slug):
    course = get_object_or_404(Course, slug=slug) if slug else None
    course.delete()
    messages.success(request, "Course deleted successfully!")
    return redirect("teacher_dashboard") 
    



