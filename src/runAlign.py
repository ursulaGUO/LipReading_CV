import whisperx
import os

# file paths
base_dir = os.path.dirname(os.path.abspath(__file__))
audio_path = os.path.join(base_dir, "../data/video_data/benchmark3.mp4")
srt_output_path = os.path.join(base_dir, "../data/video_data/benchmark3_aligned.srt")


# Try the following if you don't have nvidia gpu chip
# model = whisperx.load_model("base", device="gpu", compute_type="float16")
model = whisperx.load_model("base", device="cpu", compute_type="float32")
result = model.transcribe(audio_path, batch_size=16)

# Align to get word-level timestamps
model_a, metadata = whisperx.load_align_model(
    language_code=result["language"], device="cpu"
)
aligned_result = whisperx.align(
    result["segments"], model_a, metadata, audio_path, device="cpu"
)


# Save word timestamps to subtitle
def seconds_to_srt_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


with open(srt_output_path, "w") as f:
    for i, word in enumerate(aligned_result["word_segments"], 1):
        if "start" not in word or "end" not in word:
            print(f"Skipping word without timing info: {word}")
            continue
        start = seconds_to_srt_time(word["start"])
        end = seconds_to_srt_time(word["end"])
        f.write(f"{i}\n{start} --> {end}\n{word['word']}\n\n")


print(f"SRT saved to: {srt_output_path}")
