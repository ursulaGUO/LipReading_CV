import cv2
import mediapipe as mp
import numpy as np

# Init mediapipe
mp_face_mesh = mp.solutions.face_mesh

# Landmarks relevant to lips + jaw
selected_landmarks = [
    234, 93, 132, 58, 172, 136, 150, 149, 176, 148,
    152, 377, 400, 378, 379, 365, 397, 288, 454,
    116, 111, 117, 118, 119, 120, 121, 47, 126, 209, 
    64, 19, 278, 129, 277, 349, 348, 347, 346, 340, 345, 
    350, 355, 429, 455
]

# Load image
image_path = r"data\frame data\vid1_frame_12.png"
image = cv2.imread(image_path)

with mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5
) as face_mesh:

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_image)

    if results.multi_face_landmarks:
        h, w, _ = image.shape
        points = []

        for face_landmarks in results.multi_face_landmarks:
            for idx in selected_landmarks:
                landmark = face_landmarks.landmark[idx]
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                points.append([cx, cy])

        # Convert to numpy array
        points = np.array(points, dtype=np.int32)

        # Create a black mask
        mask = np.zeros_like(image)

        # Fill the landmark area with white
        # Instead of fillPoly:
        hull = cv2.convexHull(points)
        cv2.fillConvexPoly(mask, hull, (255, 255, 255))


        # Apply mask
        result = cv2.bitwise_and(image, mask)

        # Save result
        cv2.imwrite("data/output/face_masked.jpg", result)
        print("Saved: face_masked.jpg")

    else:
        print("No face detected.")
