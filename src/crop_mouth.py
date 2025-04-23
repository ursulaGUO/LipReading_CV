import cv2
import mediapipe as mp
import numpy as np

# suppress logging messages from mediapipe
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)

# Initialize mediapipe face mesh
mp_face_mesh = mp.solutions.face_mesh

def crop_mouth_region(image_path, save_path, selected_landmarks=[234, 152, 454], padding=0, resize=(224, 224)):
    """
    Crop the mouth region from an image using MediaPipe FaceMesh landmarks.

    Parameters:
    - image_path: str, path to the input image.
    - save_path: str, path to save the cropped output image.
    - selected_landmarks: list, list of landmark indices around the mouth and jaw.
    - padding: int, padding to add around the bounding box (default is 0).

    Returns:
    - None, but saves the cropped image to the specified path.
    """
    # Load image
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
            face_landmarks = results.multi_face_landmarks[0]
            h, w, _ = image.shape

            coords = []
            for idx in selected_landmarks:
                lm = face_landmarks.landmark[idx]
                cx, cy = int(lm.x * w), int(lm.y * h)
                coords.append((cx, cy))

            coords = np.array(coords)
            x_min, y_min = np.min(coords, axis=0)
            x_max, y_max = np.max(coords, axis=0)

            # Apply padding
            x_min = max(0, x_min - padding)
            y_min = max(0, y_min - padding)
            x_max = min(w, x_max + padding)
            y_max = min(h, y_max + padding)


            # Crop the image to the mouth+jaw region
            cropped = image[y_min:y_max, x_min:x_max]

            # resize the image before saving
            resized = cv2.resize(cropped, resize)
            # Save the cropped image
            cv2.imwrite(save_path, resized)
            print(f"Cropped image saved as {save_path}")
        else:
            print("No face detected.")



if __name__ == '__main__':
    path = r'data\frame data\vid1_frame_2.png'
    output = r'.\data\output\cropped_img.jpg'
    crop_mouth_region(path, output)