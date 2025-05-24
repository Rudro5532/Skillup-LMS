from django.shortcuts import render
from django.contrib import messages
from .models import User
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
            messages.error(request, "Password and confirm password must be same")
            return render(request, "account/student_signup.html")
        
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


def login(request):
    return render(request, "account/login.html")