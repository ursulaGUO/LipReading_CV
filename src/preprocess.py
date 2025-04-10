import cv2
import os
import numpy

# Read from data folder
project_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(project_dir, '..','data')
output_dir = os.path.join(data_dir, 'frame data')
if not os.path.exists(output_dir):
    os.mkdir(output_dir)


# Read frames of the video
video_name = f"{data_dir}/video data/Where Do We Go From Here?.mp4"
total_frame_count = 100
cap = cv2.VideoCapture(video_name)
crop_coordinates = [
    [100,30], # left top
    [500,30], # right top
    [100,150], # left bottom
    [500, 150], # right bottom
]

frame_curr = 0
while cap.isOpened() and frame_curr < total_frame_count:
    ret, frame = cap.read()

    if not ret:
        break
    
    # TODO: make the frame adjustment more automatic to capture face
    # These coefficients are fitting this one video
    # It might also work for other similar Bernie Sanders official 
    # youtube account videos.
    left = 30
    right = 400
    top = 200
    bottom = 650
    frame_croppd = frame[left:right, top:bottom]
    # TODO: make the vid1_ automatic based on video name
    frame_filename = os.path.join(output_dir, f"vid1_frame_{frame_curr}.png")
    cv2.imwrite(frame_filename, frame_croppd)
    print(f"Saved {frame_filename}")
    frame_curr += 1

cap.release()
cv2.destroyAllWindows()
print("Finished capturing all frames")

