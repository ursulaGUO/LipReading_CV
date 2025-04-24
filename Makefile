# Variables
VIDEO_PATH = "/Users/blag/Documents/UChicago MS/2025 Spring/Computer Vision with DL/LipReading_CV/data/video_data/benchmark2.mp4"
SUBTITLE_PATH = "/Users/blag/Documents/UChicago MS/2025 Spring/Computer Vision with DL/LipReading_CV/data/video_data/benchmark2_aligned.srt"
OUTPUT_DIR = "/Users/blag/Documents/UChicago MS/2025 Spring/Computer Vision with DL/LipReading_CV/data/test"
IS_SENTENCE = false

# Python environment & script
PYTHON = python3
SCRIPT = src/buildData.py

# Main target
build:
ifeq ($(IS_SENTENCE),true)
	$(PYTHON) $(SCRIPT) --video_path $(VIDEO_PATH) --subtitle_path $(SUBTITLE_PATH) --output_dir $(OUTPUT_DIR) --is_sentence
else
	$(PYTHON) $(SCRIPT) --video_path $(VIDEO_PATH) --subtitle_path $(SUBTITLE_PATH) --output_dir $(OUTPUT_DIR)
endif

# Clean target
clean:
	rm -rf $(OUTPUT_DIR)
