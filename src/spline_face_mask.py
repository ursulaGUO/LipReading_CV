import cv2
import mediapipe as mp
import numpy as np
from scipy.interpolate import splprep, splev

# Init mediapipe
mp_face_mesh = mp.solutions.face_mesh

# Landmarks relevant to lips + jaw (for example)
selected_landmarks = [
    234, 93, 132, 58, 172, 136, 150, 149, 176, 148,
    152, 377, 400, 378, 379, 365, 397, 288, 454,
    116, 111, 117, 118, 119, 120, 121, 47, 126, 209, 
    64, 19, 278, 129, 277, 349, 348, 347, 346, 340, 345, 
    350, 355, 429, 455
]

# Load image
image_path = r"data\frame data\vid1_frame_0.png"
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
        for face_landmarks in results.multi_face_landmarks:
            h, w, _ = image.shape
            points = []

            for idx in selected_landmarks:
                landmark = face_landmarks.landmark[idx]
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                points.append([cx, cy])
            
            points = np.array(points, dtype=np.float32)

            # Create smooth spline from landmark points
            tck, u = splprep([points[:, 0], points[:, 1]], s=1.0, per=True)
            unew = np.linspace(0, 1.0, 300)
            out = splev(unew, tck)
            smooth_points = np.stack([out[0], out[1]], axis=-1).astype(np.int32)

            # Create mask
            mask = np.zeros(image.shape[:2], dtype=np.uint8)
            cv2.fillPoly(mask, [smooth_points], 255)

            # Invert the mask (anti-mask)
            inv_mask = cv2.bitwise_not(mask)

            # Apply mask: black out outside area
            result = cv2.bitwise_and(image, image, mask=mask)

            # Save and show
            cv2.imwrite("data/output/smooth_mask_result.jpg", result)
            # cv2.imshow("Smooth Mask", result)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
    else:
        print("No face detected.")
