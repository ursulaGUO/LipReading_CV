# Variables
VIDEO_PATH = "/Users/blag/Documents/UChicago MS/2025 Spring/Computer Vision with DL/LipReading_CV/data/video_data/benchmark1.mp4"
SUBTITLE_PATH = "/Users/blag/Documents/UChicago MS/2025 Spring/Computer Vision with DL/LipReading_CV/data/video_data/benchmark1_aligned.srt"
OUTPUT_DIR = "/Users/blag/Documents/UChicago MS/2025 Spring/Computer Vision with DL/LipReading_CV/data/model_dataset"
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
	rm -rf $(OUTPUT_DIR)/clip_*.mp4 $(OUTPUT_DIR)/labels.csv
