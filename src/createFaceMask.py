import cv2
import mediapipe as mp
import numpy as np
import os

# Initialize MediaPipe FaceMesh
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

# Directory containing test images
input_dir = "data/frame data"
output_dir = "data/output"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Selected landmarks for creating the mask
selected_landmarks = [
    234, 93, 132, 58, 172, 136, 150, 149, 176, 148,
    152, 377, 400, 378, 379, 365, 397, 288, 454,
    116, 111, 117, 118, 119, 120, 121, 47, 126, 209, 
    64, 19, 278, 129, 277, 349, 348, 347, 346, 340, 345, 
    350, 355, 429, 455
]

def create_antimask(image, landmarks, indices):
    """Create an anti-mask based on the given landmarks."""
    h, w, _ = image.shape
    points = np.array([[int(landmarks[idx].x * w), int(landmarks[idx].y * h)] for idx in indices])
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.fillPoly(mask, [points], 255)
    anti_mask = cv2.bitwise_not(mask)
    return anti_mask

def process_image(image_path):
    """Process a single image to apply the anti-mask."""
    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_image).multi_face_landmarks

    if results:
        landmarks = results[0].landmark
        anti_mask = create_antimask(image, landmarks, selected_landmarks)
        masked_image = cv2.bitwise_and(image, image, mask=anti_mask)
        return masked_image
    return None

# Process all images in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith((".jpg", ".png")):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        processed_image = process_image(input_path)
        if processed_image is not None:
            cv2.imwrite(output_path, processed_image)
        else:
            print(f"Could not process {filename}")