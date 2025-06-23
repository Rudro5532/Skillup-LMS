from django.shortcuts import render
from django.http import JsonResponse
from .models import ContactMessage
from django.core.mail import send_mail
from django.conf import settings

def about(request):
    return render(request, "core/about.html")

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        ContactMessage.objects.create(
            name = name,
            email = email,
            message = message
        )
        send_mail(
            f"New Contact Message from {name}",
            f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
            settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_RECEIVER_EMAIL],
            fail_silently=False,
        )
        return JsonResponse({
            "success" : True,
            "message" : "Message send succesfuly"
        })

    return render(request, "core/contact.html")