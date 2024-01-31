import cv2 
import numpy as np 
  

def image_set(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    equ = cv2.equalizeHist(gray) 
    blurred = cv2.GaussianBlur(src=equ, ksize=(3, 5), sigmaX=0.5) 
    edges = cv2.Canny(blurred, 70, 135) 
    return edges

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