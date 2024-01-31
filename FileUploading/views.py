from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login , logout
from django.http import JsonResponse
from .models import User 
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.http import JsonResponse
import cv2
import numpy as np
from django.views.decorators.csrf import csrf_exempt
from rest_framework import  permissions
from .test import generate_frames
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from django.shortcuts import render



def FileUploading(request):
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")
            
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return render(request, 'navbar.html')
            else:
                return render(request, "fileupload.html", {"error": "Invalid credentials"})

        return render(request, 'fileupload.html')

def signup(request):
    if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")
            first_name = request.POST.get("first_name")
            company = request.POST.get("company")
            # Check if the email is unique
            if User.objects.filter(email=email).exists():
                return render(request, "register.html", {"error": "Email already exists"})
        
            user = User.objects.create_user(email=email, password=password, name=first_name , company=company)
            user.save()

            user = authenticate(request, username=email, password=password)
            login(request, user)
            return render(request, 'navbar.html')
    return render(request, 'login.html')

def Home(request):

    return render(request, 'navbar.html')

def how(request):
    return render(request, 'how.html')
def getFeedbackMessage(value):
    if value <= 30:
        return "Strongly Dislike"
    elif value <= 50:
        return "Dislike"
    elif value <= 70:
        return "Neutral"
    elif value <= 90:
        return "Like"
    else:
        return "Love"

def feedback(request):
    if request.method == 'POST':
        demo_rating_value = int(request.POST.get('demo_rating', 4))
        subject = request.POST.get('subject', '')
        feedback_text = request.POST.get('feedback', '')
        email = request.POST.get('email', '')
        future_projects_rating = int(request.POST.get('future_projects_rating', 1))

        feedback_message = getFeedbackMessage(demo_rating_value)
        feedback = Feedback(
            demo_rating=feedback_message, 
            subject=subject,
            feedback_text=feedback_text,
            email=email,
            future_projects_rating=future_projects_rating
        )
        feedback.save()

    return render(request, "feedback.html")


@gzip.gzip_page
def live_feed(request):
    return StreamingHttpResponse(generate_frames(), content_type="multipart/x-mixed-replace;boundary=frame")


def excercise(request):
    return render(request, 'excercise.html')


