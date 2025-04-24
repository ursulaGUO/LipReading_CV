import os
import pysrt
import csv
import subprocess
import argparse
import re

# Helper to convert subtitle timestamps to ffmpeg format
def srt_time_to_ffmpeg_time(srt_time):
    return f"{srt_time.hours:02}:{srt_time.minutes:02}:{srt_time.seconds:02}.{int(srt_time.milliseconds/10):02}"

# Helper to cut one video into mini videos based on sentence/word
def re_cutting(subs_path, video_path, output_dir, is_sentence=False):
    subs = pysrt.open(subs_path)
    if is_sentence:
        for i in range(len(subs) - 1):
            subs[i].end = subs[i + 1].start
    
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, 'labels.csv')
    with open(csv_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['filename', 'transcript'])

        for i, sub in enumerate(subs):
            start_time = srt_time_to_ffmpeg_time(sub.start)
            end_time = srt_time_to_ffmpeg_time(sub.end)
            
            transcript = sub.text.strip().replace('\n', ' ')
            title = "".join(re.findall('[\w+\']',transcript.lower()))
            file_path = os.path.join(output_dir, title)
            os.makedirs(file_path, exist_ok=True)

            clip_name = f"{i}.mp4"
            output_filename = os.path.join(file_path, clip_name)

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

            print(f"Extracting {output_filename}: {start_time} -> {end_time}")
            subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            
            writer.writerow([clip_name, transcript])

        print("All clips and labels saved.")




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract video clips using aligned subtitles.')
    parser.add_argument('--video_path', type=str, required=True, help='Path to the video file')
    parser.add_argument('--subtitle_path', type=str, required=True, help='Path to the aligned subtitle (.srt) file')
    parser.add_argument('--output_dir', type=str, required=True, help='Output directory to save clips and labels')
    parser.add_argument('--is_sentence', action='store_true', help='If set, adjusts subtitles to be sentence-level')

    args = parser.parse_args()
    
    re_cutting(args.subtitle_path, args.video_path, args.output_dir, is_sentence=args.is_sentence)