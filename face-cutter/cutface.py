




import cv2
import numpy as np
import dlib

# Load the detector
detector = dlib.get_frontal_face_detector()

# Load the image
img = cv2.imread('face-cutter/sample_canny.png')

# Convert image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = detector(gray)
# Define the offset percentage
offset_pct = 20
# Loop over the faces
for rect in faces:
    # Calculate the offset in pixels
    width_offset = int(rect.width() * offset_pct / 100)
    height_offset = int(rect.height() * offset_pct / 100)
    
    # Ensure the rectangle stays within the image bounds
    top = max(0, rect.top() - height_offset)
    left = max(0, rect.left() - width_offset)
    right = min(img.shape[1], rect.right() + width_offset)
    bottom = min(img.shape[0], rect.bottom() + height_offset)
    
    # Draw a black rectangle over the face
    cv2.rectangle(img, (left, top), (right, bottom), (255, 255, 255), -1)

# Display the output
cv2.imshow('img', img)
cv2.waitKey()