from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import User
from Courses_app.models import Category,Course
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
import re



#regex_part
name_regex = r'^([A-Za-z]{2,})(\s[A-Za-z]{2,})+$'
username_regex = r'^@([a-z0-9_]{3,})$'
email_regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
password_regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*_-])[A-Za-z\d!@#$%^&*_-]{6,}'

def student_signup(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == 'POST':
            full_name = request.POST.get("name")
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

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
                password=password
            )
            user.set_password(password)
            user.save()
            return JsonResponse({
                    "message" : "Registration success!!",
                    "success" : True
                })
        return render(request, "account/student_signup.html")


def teacher_signup(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == 'POST':
            full_name = request.POST.get("name")
            username = request.POST.get("username")
            subject = request.POST.get("subject")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

            if not all([full_name, email, password, subject, username]):
                return JsonResponse({
                    "message" : "All field ar requried",
                    "success" : False
                })

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
                subject = subject,
                email = email,
                password=password,
                is_teacher = True,
                is_staff = True
            )
            user.set_password(password)
            user.save()
            # messages.success(request ,"Registration success")
            return JsonResponse({
                "success" : True,
                "message" : "Registration success!! You are registartion as a teacher"
            })
            return render(request, "account/teacher_signup.html")
        return render(request, "account/teacher_signup.html")


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
                #print("User:", user)
                if user.is_teacher:
                    return redirect("teacher_dashboard")
                else:
                    return redirect("student_dashboard")
            else:
                messages.error(request, "Invalid credential")
                return render(request, "account/login.html")
        return render(request, "account/login.html")

@login_required
def user_logout(request):
    logout(request)
    return redirect("home")

def is_student(user):
   return user.is_authenticated and not user.is_teacher

@login_required
@user_passes_test(is_student, login_url='teacher_dashboard')
def student_dashboard(request):
    return render(request, "account/student_dashboard.html")

def is_teacher(user):
   return user.is_teacher

@login_required
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

        category = get_object_or_404(Category, id=category_id)
        teacher = get_object_or_404(User, id=teacher_id)



        create_blog = Course(
            name = name,
            category = category,
            teacher = teacher,
            price = price,
            description = description,
            slug = slug,
            image = image
        )
        create_blog.save()
        return redirect("teacher_dashboard")
    categories = Category.objects.all()
    teachers = User.objects.filter(is_teacher=True)
    context= {
        'categories' : categories,
        'teachers' : teachers
    }
    return render(request, "account/teacher_dashboard.html", context)
    


