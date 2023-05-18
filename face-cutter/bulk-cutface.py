import cv2
import dlib
import os

# Load the detector
detector = dlib.get_frontal_face_detector()

# Define the offset percentage
offset_pct = 20

# Get the directory of the script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Define the source and target directories
src_dir = os.path.join(script_dir, 'images')
dst_dir = os.path.join(script_dir, 'processed_imgs')


# Create the target directory if it doesn't exist
os.makedirs(dst_dir, exist_ok=True)

# Iterate over the images in the source directory
for filename in os.listdir(src_dir):
    # Skip non-image files
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue

    # Load the image
    img = cv2.imread(os.path.join(src_dir, filename))

    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = detector(gray)

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
        cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 0), -1)

    # Save the processed image to the target directory
    cv2.imwrite(os.path.join(dst_dir, filename), img)