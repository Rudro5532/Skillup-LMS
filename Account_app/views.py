from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import User,PasswordResetOtp
from Courses_app.models import Category,Course,CourseVideo
from Payment_app.models import Payment
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .authentication import create_access_token,create_refresh_token
from django.contrib.auth.hashers import check_password,make_password
import re
import os
import random
from dotenv import load_dotenv
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.views.decorators.cache import never_cache

load_dotenv()

#regex_part
name_regex = r'^([A-Za-z]{2,})(\s[A-Za-z]{2,})+$'
username_regex = r'^@([a-z0-9_]{3,})$'
email_regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
password_regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*_-])[A-Za-z\d!@#$%^&*_-]{6,}'
# for registration
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

            errors = {}

            if not full_name:
                errors['name'] = "Name is required"

            elif not re.fullmatch(name_regex, full_name):
                errors['name'] = "Please write your full and correct name"

            if not password:
                errors['password'] = "Password is required"
            elif not re.fullmatch(password_regex,password):
                errors['password'] = "write minimum 6 chracter of password. Minimum one capital letter one small letter one digit and one special charecter."

            if not confirm_password:
                errors['confirm_password'] = "Password and confirm_password both are required"

            if password != confirm_password:
                errors['password'] = "password and confirm password must be same"
            
            if User.objects.filter(email=email).exists():
                errors['email'] = "Email already exists"
            elif not email:
                errors['email'] = "Email is required"
            elif not re.fullmatch(email_regex, email):
                errors['email'] = "Please write correct format of email"

            
            if User.objects.filter(username=username).exists():
                errors['username'] = "Username already registered"

            if not username:
                errors['username'] = "username required"
            elif not re.fullmatch(username_regex,username):
                errors['username'] = "Start with @ and use one number and always use small letter"

            if is_teacher and not subject:
                errors['subject'] = "subject required"


            if errors:
                return JsonResponse({"success": False, "errors": errors})

                
            user = User(
                full_name = full_name,
                username = username,
                email = email,
                password=password,
                subject = subject,
                is_teacher = is_teacher,
                is_staff = is_staff,
            )
            user.set_password(password)
            user.save()
            try:
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                activation_link = f"http://localhost:8000/account/activate/{uidb64}/{token}/"
                subject_line = "Activate your Skillup account"
                from_email = settings.EMAIL_HOST_USER
                to_email = [email]
                message = render_to_string('account/email.html',{
                    'activation_link' : activation_link,
                    'name' : full_name,
                })
                text_content = strip_tags(message)
                email_message = EmailMultiAlternatives(subject_line, text_content, from_email, to_email)
                email_message.attach_alternative(message, 'text/html')
                email_message.send()
                return JsonResponse({"message": "Registration successful! Check your email to activate.", "success": True})

            except Exception as e:
                user.delete()
                return JsonResponse({"message": "Email sending failed. Try again.", "success": False})

    return render(request, "account/signup.html")
    
# account activation link
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

# for user_login
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

# for logout user
@login_required(login_url="home")
def user_logout(request):
    logout(request)
    return redirect("home")

# define the function as student
def is_student(user):
   return user.is_authenticated and not user.is_teacher

# student dashboard
@never_cache
@login_required(login_url="user_login")
@user_passes_test(is_student, login_url='teacher_dashboard')
def student_dashboard(request):
    enroll_courses = Payment.objects.filter(user=request.user, is_paid=True)
    context = {
        'enroll_courses' : enroll_courses
    }
    return render(request, "account/student_dashboard.html", context)

# define the function as teacher
def is_teacher(user):
   return user.is_teacher

# teacher dashboard
@never_cache
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
            "message" : "Course published successfully",
            "redirect_url" : "/account/teacher_dashboard/"
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
        'students' : students,
    }
    return render(request, "account/teacher_dashboard.html", context)

@login_required(login_url="user_login")
@user_passes_test(is_teacher, login_url='home')
def course_video(request):
    if request.method == 'POST':
        title = request.POST.get("title")
        course_id = request.POST.get("course_name")
        video_file = request.FILES.get("video_file")

        errors = {}

        if not title:
            errors['title'] = "Video title required"

        if not course_id:
            errors['course_name'] = "Select your course name"

        if not video_file:
            errors['video_file'] = "Video file required"

        if errors:
            return JsonResponse({"success": False, "errors": errors})

        course = get_object_or_404(Course, id=course_id, teacher=request.user)

        video_create = CourseVideo.objects.create(
            title=title,
            course=course,
            video=video_file
        )
        video_create.save()
        return JsonResponse({
            "message" : "Video upload successfully !!",
            "success" : True,
            "redirect_url" : "/account/course_video/"
        })
    courses = Course.objects.filter(teacher=request.user)       
    return render(request, "account/video.html", {"courses" : courses})

# for edit video
@login_required(login_url='user_login')
@user_passes_test(is_teacher, login_url='home')
def edit_course_video(request,id):
    course_video = get_object_or_404(CourseVideo, id=id)

    if course_video.course.teacher != request.user:
        return JsonResponse({
            "message" : "You don't have permission to edit this video",
            "success" : False
        })
    if request.method == 'POST':
        title = request.POST.get("title")
        course_id = request.POST.get("course_name")
        video_file = request.FILES.get("video_file")

        if not (title and course_id):
            return JsonResponse({
                "message": "All fields are required",
                "success": False
            })
        
        course = get_object_or_404(Course, id=course_id, teacher=request.user)
        course_video.title = title
        course_video.course = course
        if video_file:
            course_video.video = video_file
        course_video.save()
        return JsonResponse({
            "message" : "Course update successfully !!",
            "success" : True,
            "redirect_url" : "/account/course_video/"
        })
    courses = Course.objects.filter(teacher=request.user)
    return render(request, "account/video.html", {
        "video": course_video,
        "courses": courses,
    })

# for delete course video
@login_required(login_url='user_login')
@user_passes_test(is_teacher, login_url='home')
@require_POST
def delete_course_video(request,id):
    course_video = get_object_or_404(CourseVideo, id=id)

    if course_video.course.teacher != request.user:
        return JsonResponse({
            "message" : "You don't have permission to delete this video",
            "success" : False
        })
    try:
        if course_video:
            course_video.delete()
            return JsonResponse({
                    "message" : "Video delete successfully !! ",
                    "redirect_url" : "/account/course_video/",
                    "success" : True,
                })
    except PermissionError:
        return JsonResponse({
            "message": "Video file is currently in use. Please close any open players and try again.",
            "success": False
        })

# for edit courses
@login_required(login_url='user_login')
@user_passes_test(is_teacher, login_url='home')
def edit_course(request, slug):
    course = get_object_or_404(Course, slug=slug) if slug else None
    if course.teacher != request.user:
        return JsonResponse({
            "error": "You don't have permission to edit this course."
        }, status=403)
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
            "message": "Course updated successfully",
            "redirect_url" : '/account/teacher_dashboard/'
        })

    teachers = User.objects.filter(is_teacher=True)
    courses = Course.objects.filter(teacher=request.user)
    categories = Category.objects.all()
    enrollments = Payment.objects.select_related('enrollment__user', 'course')\
    .filter(course=course, status='Completed', is_paid=True)
    context = {
        'categories': categories,
        'teachers': teachers,
        'courses': courses,
        'course_details': course,
        'enrollments': enrollments,
    }
    return render(request, "account/teacher_dashboard.html", context)

# for delete courses
@login_required(login_url='user_login')
@user_passes_test(is_teacher, login_url='home')
@require_POST
def delete_course(request, slug):
    course = get_object_or_404(Course, slug=slug) if slug else None
    if course.teacher != request.user:
        return JsonResponse({
            "error": "You don't have permission to delete this course."
        }, status=403)
    course.delete()
    return JsonResponse({
        "message" : "Course Delete Successfully",
        "success" : True,
        "redirect_url" : "/account/teacher_dashboard/"
    })

# all student list
@login_required(login_url='user_login')
@user_passes_test(is_teacher, login_url='home')
def enrolled_students_list(request):
    enrollments = Payment.objects.filter(is_paid=True).select_related('user', 'course')
    context = {
        'enrollments': enrollments
    }
    return render(request, 'account/student_list.html', context)

# for edit profile
@login_required(login_url='user_login')
def edit_profile(request):
    user = request.user

    if request.method == "POST":
        user.username = request.POST.get("username")
        user.full_name = request.POST.get("fullname")

        if not re.fullmatch(name_regex, user.full_name):
                return JsonResponse({
                    "message" : "Please write your full and correct name",
                    "success" : False
            })
        
        if not re.fullmatch(username_regex, user.username):
                return JsonResponse({
                    "message" : "Start with @ and use one number and always use small letter",
                    "success" : False
            })
        
        if request.FILES.get("profile_image"):
            user.profile_image = request.FILES.get("profile_image")

        user.save()
        return JsonResponse({
            "success" : True,
            "message" : "Profile updated successfully",
            "redirect_url" : "/account/teacher_dashboard/" if user.is_teacher else "/account/student_dashboard/"
        })

    context = {
        "user" : user
    }
    return render(request, 'account/edit_profile.html', context)

# for change password
@login_required(login_url="user_login")
def change_password(request):
    user = request.user
    if request.method == "POST":
        currentPassword = request.POST.get("currentPassword")
        newPassword = request.POST.get("newPassword")
        confirmPassword = request.POST.get("confirmPassword")

        if not re.fullmatch(password_regex, newPassword):
            return JsonResponse({
                "message" : "write minimum 6 chracter of password. Minimum one capital letter one small letter one digit and one special charecter.",
                "success" : False
            })

        if not check_password(currentPassword ,user.password):
            return JsonResponse({
                "success" : False,
                "message" : "current password dosen't match.",
            })
        if newPassword == confirmPassword:
            print("newpass", newPassword)
            print("confirm", confirmPassword)
            user.set_password(newPassword)
            user.save()
            return JsonResponse({
                "success" : True,
                "message" : "Password Change Successfully",
                "redirect_url" :"/account/teacher_dashboard/" if user.is_teacher else "/account/student_dashboard/"
            })
        else:
           return JsonResponse({
                "success" : False,
                "message" : "New password and confirm password dosen't match",
            })
    return render(request, "account/change_password.html")

# for otp
def send_otp_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            otp = str(random.randint(100000, 999999))
            while PasswordResetOtp.objects.filter(otp=otp).exists():
                otp = str(random.randint(100000, 999999))

            PasswordResetOtp.objects.create(user=user,otp=otp)

            send_mail(
                subject= "Your reset password OTP",
                message = f"Your OTP is {otp}",
                from_email= settings.EMAIL_HOST_USER,
                recipient_list=[email], 
                fail_silently=False
            )
            return JsonResponse({
                "success" : True,
                "message" : "OTP send on your email",
                "redirect_url" : "/account/reset_password/"
            })
        
        except User.DoesNotExist:
            return JsonResponse({
                "success" : False,
                "message" : "user dosen't exist!"
            })
    return render(request, "account/otp.html")

# for rest password
def reset_password(request):
    if request.method == "POST":
        otp = request.POST.get("otp")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_new_password")

        if new_password != confirm_password:
            return JsonResponse({
                "success": False,
                "message": "Passwords do not match."
            })
        
        if not re.fullmatch(password_regex, new_password ):
            return JsonResponse({
                "message" : "write minimum 6 chracter of password. Minimum one capital letter one small letter one digit and one special charecter.",
                "success" : False
            })
        try:
            otp_entry = PasswordResetOtp.objects.filter(otp=otp).order_by('-created_at').first()

            if otp_entry and otp_entry.is_valid():
                user = otp_entry.user
                user.password = make_password(new_password)
                user.save()
                otp_entry.delete()
                return JsonResponse({
                    "success": True,
                    "message": "Password reset successfully!",
                    "redirect_url": "/account/user_login/"
                })
            else:
                return JsonResponse({
                    "success": False,
                    "message": "Invalid or expired OTP."
                })
        except Exception as e:
            print("RESET PASSWORD ERROR:", e)
            return JsonResponse({
                "success": False,
                "message": "Something went wrong."
            })

    return render(request, "account/reset_password.html")


#for admin registration
def admin_reg(request):
    if request.method == "POST":
        full_name = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return JsonResponse({
                "message": "Password and confirm password must be same",
                "success": False
            })

        if User.objects.filter(email=email).exists():
            return JsonResponse({
                "message": "Email already registered",
                "success": False
            })

        if not re.fullmatch(password_regex, password):
            return JsonResponse({
                "message": "Write minimum 6 characters. Must contain uppercase, lowercase, digit and special character.",
                "success": False
            })

        if not re.fullmatch(name_regex, full_name):
            return JsonResponse({
                "message": "Please write your full and correct name",
                "success": False
            })

        if not re.fullmatch(username_regex, username):
            return JsonResponse({
                "message": "Start with @, use one number, and all small letters",
                "success": False
            })

        if not re.fullmatch(email_regex, email):
            return JsonResponse({
                "message": "Please write correct format of email",
                "success": False
            })

        user = User(
            full_name=full_name,
            username=username,
            email=email,
            is_superuser=True,
            is_staff=True,
            is_active =True
        )
        user.set_password(password)
        user.save()
        return JsonResponse({
            "message": "Registration successfull !!",
            "success": True
        })

    return render(request, "account/admin_reg.html")



    



