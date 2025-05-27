from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
import re



#regex_part

name_regex = r'^([A-Za-z]{2,})(\s[A-Za-z]{2,})+$'
username_regex = r'^@([a-z0-9_]{3,})$'
email_regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
password_regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*_-])[A-Za-z\d!@#$%^&*_-]{6,}'

def student_signup(request):
    if request.method == 'POST':
        full_name = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not password == confirm_password:
            #messages.error(request, "Password and confirm password must be same")
            return JsonResponse({
                "acknowledge" : "Password and confirm password must be same"
            })
            #return render(request, "account/student_signup.html")
        
        if User.objects.filter(email=email).exists():
            messages.error(request , "Email already register")
            return render(request, "account/student_signup.html")

        
        if not re.fullmatch(password_regex, password ):
            messages.error(request ,"write minimum 6 chracter of password. Minimum one capital letter one small letter one digit and one special charecter.")
            return render(request, "account/student_signup.html")
        
        if not re.fullmatch(name_regex, full_name):
            messages.error(request ,"Please write your full and correct name")
            return render(request, "account/student_signup.html")
        
        if not re.fullmatch(username_regex,username):
            messages.error(request ,"Start with @ and use one number and always use small letter")
            return render(request, "account/student_signup.html")
        
        if not re.fullmatch(email_regex, email):
            messages.error(request ,"Please write correct format of name")
            return render(request, "account/student_signup.html")
        
        user = User(
            full_name = full_name,
            username = username,
            email = email,
            password=password
        )
        user.set_password(password)
        user.save()
        messages.success(request ,"Registration success")
        return render(request, "account/student_signup.html")
    return render(request, "account/student_signup.html")


def teacher_signup(request):
    if request.method == 'POST':
        full_name = request.POST.get("name")
        username = request.POST.get("username")
        subject = request.POST.get("subject")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not all([full_name, email, password, subject, username]):
            messages.error(request, "All field ar required")
            return render(request, "account/teacher_signup.html")

        if not password == confirm_password:
            messages.error(request, "Password and confirm password must be same")
            return render(request, "account/teacher_signup.html")
        
        if User.objects.filter(email=email).exists():
            messages.error(request , "Email already register")
            return render(request, "account/teacher_signup.html")

        
        if not re.fullmatch(password_regex, password ):
            messages.error(request ,"write minimum 6 chracter of password. Minimum one capital letter one small letter one digit and one special charecter.")
            return render(request, "account/teacher_signup.html")
        
        if not re.fullmatch(name_regex, full_name):
            messages.error(request ,"Please write your full and correct name")
            return render(request, "account/teacher_signup.html")
        
        if not re.fullmatch(username_regex,username):
            messages.error(request ,"Start with @ and use one number and always use small letter")
            return render(request, "account/teacher_signup.html")
        
        if not re.fullmatch(email_regex, email):
            messages.error(request ,"Please write correct format of name")
            return render(request, "account/teacher_signup.html")
        
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
        messages.success(request ,"Registration success")
        return render(request, "account/teacher_signup.html")
    return render(request, "account/teacher_signup.html")


def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email = email, password = password)
        if user is not None:
            login(request, user)
            print("User:", user)
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
    return render(request, "account/teacher_dashboard.html")


