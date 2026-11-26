"""
kaggle_kernel_generate.py  (adapted for Sanju's Hindi taxi reel)
Runs INSIDE a Kaggle Notebook (GPU: T4, forced via orchestrator.py's machine_shape).

Adapted from: https://github.com/soumyabandi252/mytho-verse-video-gen
Original: ~60s mythology video (Krishna + baby), landscape, English narration.
This version: ~60s Hindi taxi mini-film, vertical 9:16 for YouTube Shorts,
Hindi narration, 5 story beats x 3 clips each.

Pipeline:
  1. Install/upgrade required packages.
  2. Generate two reference images (woman in beige coat, man in black puffer
     jacket) with SDXL-Turbo (open, ungated, T4-light).
  3. For each of the 5 story beats, animate the beat's reference image into
     3 x ~4s clips with Stable Video Diffusion (img2vid-xt), so the two
     characters stay roughly consistent across the video.
  4. Generate Hindi narration audio with VitsModel (facebook/mms-tts-hin).
  5. Stitch everything with ffmpeg into output.mp4 (Kaggle kernel output).

Honest limits (same as the original pipeline):
  - Character consistency is approximate; open-weight models have no
    face-lock like paid tools (Kling, Veo).
  - SVD clips are gentle motion (camera drift, rain, movement), not acted
    dialogue with lip-sync. The story is carried by the narration,
    captions and the edit, not by the actors speaking on camera.
  - Vertical 576x1024 is adapted from the original's landscape 1024x576
    and is untested on the first run; if SVD rejects the shape, the
    fallback is landscape + crop to 9:16 in the edit.
  - First run is slow due to ~15GB of model weight downloads.

Kaggle settings required:
  - GPU type is forced to T4 via "machine_shape" in orchestrator.py.
  - Internet: ON (requires phone verification on your Kaggle account).
  - Kernel type: "Script", so it runs headless via `kaggle kernels push`.
"""

import subprocess
import sys

print("Installing/upgrading required packages...")
subprocess.run(
    [sys.executable, "-m", "pip", "install", "-q", "-U",
     "diffusers>=0.31.0", "transformers>=4.44.0", "accelerate>=0.33.0",
     "imageio-ffmpeg", "sentencepiece", "protobuf", "scipy"],
    check=True
)

import os
import json
import traceback
import gc

import torch
import scipy.io.wavfile
from diffusers import AutoPipelineForText2Image, StableVideoDiffusionPipeline
from diffusers.utils import export_to_video, load_image
from transformers import VitsModel, AutoTokenizer

PROMPT = os.environ.get(
    "SCENE_PROMPT",
    "A young Indian woman hails a yellow taxi in the rain at night, a man steals it, twist: he is her father"
)

# 5 story beats, 3 clips each, ~4s per clip = ~60s total.
BEATS = [
    {"name": "rain-street", "ref": "woman",
     "image": "Young Indian woman in a beige coat waving to hail a yellow taxi on a rainy night street, wet road reflections, street lights, front-facing portrait, highly detailed digital painting style"},
    {"name": "the-steal", "ref": "man",
     "image": "Middle-aged Indian man in a black puffer jacket stepping into a yellow taxi with a smug smile, rainy night, front-facing portrait, highly detailed digital painting style"},
    {"name": "the-chase", "ref": "woman",
     "image": "Young Indian woman in a beige coat running after a yellow taxi in the rain at night, determined angry expression, front-facing portrait, highly detailed digital painting style"},
    {"name": "the-twist", "ref": "man",
     "image": "Middle-aged Indian man in a black puffer jacket smiling warmly inside a yellow taxi at night, rain on the windows, front-facing portrait, highly detailed digital painting style"},
    {"name": "the-laugh", "ref": "woman",
     "image": "Young Indian woman laughing warmly in the back seat of a yellow taxi at night, rain on the window, warm light, front-facing portrait, highly detailed digital painting style"},
]
CLIPS_PER_BEAT = 3
SVD_NUM_FRAMES = 25
SVD_FPS = 6
WORKDIR = "/kaggle/working"
os.makedirs(WORKDIR, exist_ok=True)

# Vertical 9:16 for YouTube Shorts.
IMG_WIDTH = 576
IMG_HEIGHT = 1024

DTYPE = torch.float16  # T4-safe dtype


def free_gpu():
    gc.collect()
    torch.cuda.empty_cache()
    torch.cuda.ipc_collect()


def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    if device == "cpu":
        raise RuntimeError("No GPU available - this pipeline requires a GPU kernel.")

    gpu_name = torch.cuda.get_device_name(0)
    total_vram = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
    print(f"GPU: {gpu_name}, VRAM: {total_vram:.1f} GB")
    if "P100" in gpu_name:
        raise RuntimeError(
            "This kernel is running on a P100, which is incompatible with the current "
            "PyTorch build (dropped sm_60 support). Check machine_shape in orchestrator.py."
        )

    print("Loading SDXL-Turbo for reference images (open, ungated, memory-optimized)...")
    img_pipe = AutoPipelineForText2Image.from_pretrained(
        "stabilityai/sdxl-turbo", torch_dtype=DTYPE, variant="fp16", low_cpu_mem_usage=True
    )
    img_pipe.enable_model_cpu_offload()
    img_pipe.vae.enable_slicing()
    img_pipe.vae.enable_tiling()

    ref_paths = {}
    for ref in ("woman", "man"):
        beat = next(b for b in BEATS if b["ref"] == ref)
        ref_path = f"{WORKDIR}/{ref}_ref.png"
        print(f"Generating reference image: {ref}")
        img = img_pipe(
            beat["image"],
            num_inference_steps=2, guidance_scale=0.0,
            height=IMG_HEIGHT, width=IMG_WIDTH,
        ).images[0]
        img.save(ref_path)
        ref_paths[ref] = ref_path

    del img_pipe
    free_gpu()
    gc.collect()

    print("Loading Stable Video Diffusion (img2vid-xt, T4-light)...")
    video_pipe = StableVideoDiffusionPipeline.from_pretrained(
        "stabilityai/stable-video-diffusion-img2vid-xt",
        torch_dtype=DTYPE, variant="fp16", low_cpu_mem_usage=True
    )
    video_pipe.enable_model_cpu_offload()

    clip_paths = []
    for beat in BEATS:
        ref_path = ref_paths[beat["ref"]]
        for j in range(CLIPS_PER_BEAT):
            clip_index = len(clip_paths)
            ref_image = load_image(ref_path).resize((IMG_WIDTH, IMG_HEIGHT))
            print(f"Generating clip {clip_index + 1}/15: beat {beat['name']} clip {j + 1}")
            frames = video_pipe(
                ref_image,
                num_frames=SVD_NUM_FRAMES,
                decode_chunk_size=8,
                motion_bucket_id=110 + j * 15,
                noise_aug_strength=0.02,
            ).frames[0]
            clip_path = f"{WORKDIR}/scene_{clip_index:02d}.mp4"
            export_to_video(frames, clip_path, fps=SVD_FPS)
            clip_paths.append(clip_path)
            free_gpu()

    del video_pipe
    free_gpu()
    gc.collect()

    print("Loading VitsModel directly for Hindi narration (facebook/mms-tts-hin)...")
    tts_model = VitsModel.from_pretrained("facebook/mms-tts-hin").to(device)
    tts_tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-hin")

    narration_text = (
        "Baarish wali raat. Ek taxi. Ye meri taxi thi! "
        "Zara tez hona chahiye tha, sweetheart. "
        "Arey, sambhal ke. Thand lag jayegi. "
        "Papa? AAP? Beta, taxi to maine hi book ki thi. Papa bhi na."
    )
    tts_inputs = tts_tokenizer(narration_text, return_tensors="pt").to(device)
    with torch.no_grad():
        waveform = tts_model(**tts_inputs).waveform

    narration_path = f"{WORKDIR}/narration.wav"
    scipy.io.wavfile.write(
        narration_path,
        rate=tts_model.config.sampling_rate,
        data=waveform.float().cpu().numpy().squeeze()
    )

    del tts_model, tts_tokenizer
    free_gpu()

    shifted_narration = f"{WORKDIR}/narration_shifted.wav"
    subprocess.run([
        "ffmpeg", "-y", "-i", narration_path,
        "-af", "asetrate=44100*0.95,aresample=44100,atempo=1.05",
        shifted_narration
    ], check=True)

    concat_list_path = f"{WORKDIR}/concat_list.txt"
    with open(concat_list_path, "w") as f:
        for p in clip_paths:
            f.write(f"file '{p}'\n")

    silent_full_path = f"{WORKDIR}/full_silent.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_list_path, "-c", "copy", silent_full_path
    ], check=True)

    final_output = f"{WORKDIR}/output.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-i", silent_full_path, "-i", shifted_narration,
        "-c:v", "copy", "-c:a", "aac", "-shortest", final_output
    ], check=True)

    print(f"Done. Final video at: {final_output}")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("FATAL ERROR IN PIPELINE:")
        traceback.print_exc()
        sys.exit(1)
