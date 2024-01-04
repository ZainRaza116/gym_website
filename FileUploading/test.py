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

