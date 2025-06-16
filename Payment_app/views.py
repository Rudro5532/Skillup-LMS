from django.shortcuts import render
import razorpay
import time
import razorpay.errors
import requests.exceptions
from django.http import JsonResponse
from intelligent_LMS import settings
from Courses_app.models import Enrollment
from .models import Payment
from Courses_app.models import Course

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
def course_enrolled(request):
    if request.method == "POST":
        try:
            amount = int(request.POST.get("amount")) * 100
            course_id = request.POST.get("course_id")
            print("Amount recived :", amount)

            if not course_id:
                return JsonResponse({"error": "Course ID missing."})

            if not amount or amount <= 0:
                return JsonResponse({
                    "response" : False,
                    "error" : "Please enter valid amount"
                })
            course = Course.objects.get(id=course_id) 
            order_data = {
                "amount" : amount,
                "currency" : "INR",
                "payment_capture" : True,
            }

            for _ in range(3):
                try:
                    order_response = client.order.create(order_data)
                    print("order respone :", order_response)
                    break
                except razorpay.errors.RazorpayError as e:
                    print("Razorpay error : ", str(e))
            if 'id' not in order_response:
                return JsonResponse({"error": "Failed to create Razorpay order."})
            
            enrollment = Enrollment.objects.create(
                user = request.user,
                total_price = amount / 100,
                razorpay_order_id = order_response['id'],
                course=course
            )

            Payment.objects.create(
                user = request.user,
                enrollment = enrollment,
                amount = amount / 100,
                payment_method = 'Razorpay',
                status = 'Pending',
                transaction_id = order_response['id']
            )
            return JsonResponse({
                "order_id": order_response['id'],
                "key": settings.RAZORPAY_KEY_ID,
                "amount": amount,
                "name" : course.name
            })
        except Exception as e:
            return JsonResponse({"error" : str(e)})
    return JsonResponse({
        "error" : "Invalid request"
    })


def verify_payment(request):
    if request.method == "POST":
        try :
            data = request.POST
            print("Recived Data :", data)

            razorpay_order_id = data.get("razorpay_order_id")
            razorpay_payment_id = data.get("razorpay_payment_id")
            razorpay_signature = data.get("razorpay_signature")

            if not(razorpay_order_id and razorpay_payment_id and razorpay_signature):
                return JsonResponse({"error": "Missing required payment details."})
            
            params_dict = {
                "razorpay_order_id" : razorpay_order_id,
                "razorpay_payment_id" : razorpay_payment_id,
                "razorpay_signature" : razorpay_signature
            }

            try:
                client.utility.verify_payment_signature(params_dict)
                print("Payment verification successfull")

                payment = Payment.objects.get(transaction_id=razorpay_order_id)
                payment.status = "Completed"
                payment.is_paid = True
                payment.save()
                return JsonResponse({"success": True, "message": "Payment verified successfully!"})
            except razorpay.errors.SignatureVerificationError:
                print("Signature verification failed!")
                return JsonResponse({"error": "Invalid payment signature."})
        except Exception as e:
            print("Error:", str(e))
            return JsonResponse({"error": str(e)})
    return JsonResponse({"error": "Invalid request method"})
