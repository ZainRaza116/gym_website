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

        feedback_message = getFeedbackMessage(demo_rating_value)  # Get feedback message
        feedback = Feedback(
            demo_rating=feedback_message,  # Use feedback message here
            subject=subject,
            feedback_text=feedback_text,
            email=email,
            future_projects_rating=future_projects_rating
        )
        feedback.save()

    return render(request, "feedback.html")

import cv2 
  
# import Numpy 
import numpy as np 
  

def image_set(img):
    # creating a Histograms Equalization 
    # of a image using cv2.equalizeHist() 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    equ = cv2.equalizeHist(gray) 
    
    # stacking images side-by-side 
    #res = np.hstack((equ, equ)) 

    
      
    # Apply Gaussian blur to reduce noise and smoothen edges 
    blurred = cv2.GaussianBlur(src=equ, ksize=(3, 5), sigmaX=0.5) 
      
    # Perform Canny edge detection 
    edges = cv2.Canny(blurred, 70, 135) 

    return edges



from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from django.shortcuts import render

cap = cv2.VideoCapture(0)
def generate_frames():
    while True:
        success, frame = cap.read()

        if not success:
            break
        else:
            # Apply image processing to the frame
            processed_frame = image_set(frame)

            # Encode the processed frame to JPEG format
            _, buffer = cv2.imencode('.jpg', processed_frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@gzip.gzip_page
def live_feed(request):
    return StreamingHttpResponse(generate_frames(), content_type="multipart/x-mixed-replace;boundary=frame")
def excercise(request):
    return render(request, 'excercise.html')


