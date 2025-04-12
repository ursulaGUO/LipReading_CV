import os
import pysrt
import csv
import subprocess

# Define paths
video_path = '/Users/blag/Documents/UChicago MS/2025 Spring/Computer Vision with DL/LipReading_CV/data/video_data/benchmark1.mp4'
subtitle_path = '/Users/blag/Documents/UChicago MS/2025 Spring/Computer Vision with DL/LipReading_CV/data/video_data/benchmark1_aligned.srt'
output_dir = '/Users/blag/Documents/UChicago MS/2025 Spring/Computer Vision with DL/LipReading_CV/data/model_dataset'


os.makedirs(output_dir, exist_ok=True)
subs = pysrt.open(subtitle_path)

'''#Necessary for sentence subtitles, but not needed for word subtitles

# Adjust subtitles: make each end time = next start time (except last)
for i in range(len(subs) - 1):
    subs[i].end = subs[i + 1].start
'''


# Helper to convert subtitle timestamps to ffmpeg format
def srt_time_to_ffmpeg_time(srt_time):
    return f"{srt_time.hours:02}:{srt_time.minutes:02}:{srt_time.seconds:02}.{int(srt_time.milliseconds/10):02}"

csv_path = os.path.join(output_dir, 'labels.csv')
with open(csv_path, mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['filename', 'transcript']) 

    for i, sub in enumerate(subs):
        start_time = srt_time_to_ffmpeg_time(sub.start)
        end_time = srt_time_to_ffmpeg_time(sub.end)
        clip_name = f"clip_{i:04d}.mp4"
        output_filename = os.path.join(output_dir, clip_name)

        command = [
            "ffmpeg",
            "-y",
            "-i", video_path,
            "-ss", start_time,
            "-to", end_time,
            "-c:v", "libx264",
            "-c:a", "aac",
            output_filename
        ]


        print(f"Extracting {clip_name}: {start_time} -> {end_time}")
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        transcript = sub.text.strip().replace('\n', ' ')
        writer.writerow([clip_name, transcript])

print("All clips and labels saved.")