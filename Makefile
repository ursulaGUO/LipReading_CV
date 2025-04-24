# Variables

# Path
VIDEO_PATH = "/Users/blag/Documents/UChicago MS/2025 Spring/Computer Vision with DL/LipReading_CV/data/video_data/benchmark2.mp4"
OUTPUT_VIDEO_PATH = "/Users/blag/Documents/UChicago MS/2025 Spring/Computer Vision with DL/LipReading_CV/data/video_data/benchmark2_cropped.mp4"
SUBTITLE_PATH = "/Users/blag/Documents/UChicago MS/2025 Spring/Computer Vision with DL/LipReading_CV/data/video_data/benchmark2_aligned.srt"
OUTPUT_DIR = "/Users/blag/Documents/UChicago MS/2025 Spring/Computer Vision with DL/LipReading_CV/data/test"

# Argument for clipping into mini videos
IS_SENTENCE = false

# Argument for cropping video size
# ffmpeg -i in.mp4 -vf "crop=out_w:out_h:x:y" out.mp4
CROP_X = 0 # Top left corner x
CROP_Y = 0 # Top left corner x
OUT_W = 1800 # Width of desired video
OUT_H = 750 # Height of desired video

# Python environment & script
PYTHON = python3
SCRIPT = src/buildData.py

# clip for clipping one video into smaller videos
clip:
ifeq ($(IS_SENTENCE),true)
	$(PYTHON) $(SCRIPT) --video_path $(VIDEO_PATH) --subtitle_path $(SUBTITLE_PATH) --output_dir $(OUTPUT_DIR) --is_sentence
else
	$(PYTHON) $(SCRIPT) --video_path $(VIDEO_PATH) --subtitle_path $(SUBTITLE_PATH) --output_dir $(OUTPUT_DIR)
endif

# crop for cropping one video into another video
crop:
	ffmpeg -i $(VIDEO_PATH) -vf "crop=$(OUT_W):$(OUT_H):$(CROP_X):$(CROP_Y)" $(OUTPUT_VIDEO_PATH)

# Clean target
clean:
	rm -rf $(OUTPUT_DIR)
