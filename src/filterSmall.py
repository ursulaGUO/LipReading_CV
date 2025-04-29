import os
import glob
import argparse
import shutil

def clean_small_folders(base_dir, min_files=5):
    for folder_name in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder_name)
        if os.path.isdir(folder_path):
            mp4_files = glob.glob(os.path.join(folder_path, "*.mp4"))
            if len(mp4_files) < min_files:
                print(f"Deleting folder '{folder_path}' with only {len(mp4_files)} .mp4 files.")
                shutil.rmtree(folder_path)
    print("Cleanup completed.")

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        description="Extract video clips using aligned subtitles."
    )
    parser.add_argument(
        "--video_path", type=str, required=True, help="Path to the video file"
    )
    args = parser.parse_args()
    clean_small_folders(args.video_path)
