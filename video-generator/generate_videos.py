"""
Nairu AI Video Generator — Veo 3.1 via Gemini API
Generates promotional videos using Google Veo 3.1 with reference images.
Requires: google-genai, GEMINI_API_KEY environment variable
"""

import os
import sys
import time
import base64
from pathlib import Path
from dotenv import load_dotenv

# Load .env from telegram-bot dir (shares the same API key)
env_path = Path(__file__).parent.parent / "telegram-bot" / ".env"
load_dotenv(env_path)

from google import genai
from google.genai import types

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY not found in .env")
    sys.exit(1)

client = genai.Client(api_key=GEMINI_API_KEY)

# Output directory
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Reference images directory
IMAGES_DIR = Path(__file__).parent.parent / "landing-page" / "assets" / "images"


def load_image(path: str) -> types.Image:
    """Load a local image file as a types.Image for the API."""
    img_path = Path(path)
    with open(img_path, "rb") as f:
        image_bytes = f.read()
    return types.Image(image_bytes=image_bytes, mime_type="image/png")


# ============================================================
# VIDEO PROMPTS — Nairu themed content
# ============================================================
VIDEO_PROMPTS = [
    {
        "name": "nairu_gaming_intro",
        "prompt": (
            "A beautiful Brazilian woman in her late 20s with long straight black hair "
            "and fair skin, wearing a dark hoodie, sits in a high-tech gaming room with "
            "purple and pink neon lights. She slowly turns to the camera and smiles "
            "warmly. RGB keyboard and multiple monitors glow behind her. Cinematic "
            "lighting, photorealistic, shallow depth of field. The camera slowly "
            "pushes in towards her face."
        ),
        "reference_image": "hero.png",
        "aspect_ratio": "9:16",   # Reels/Stories format
        "duration": 5,
    },
    {
        "name": "nairu_selfie_vlog",
        "prompt": (
            "A beautiful woman with long straight black hair takes a selfie-style "
            "video. She winks at the camera and blows a kiss, with a playful smile. "
            "Soft natural lighting with purple ambient backlights. Her hair gently "
            "sways. Close-up shot, warm color grading, cinematic bokeh background. "
            "Photorealistic, 4K quality."
        ),
        "reference_image": "gallery2.png",
        "aspect_ratio": "9:16",
        "duration": 5,
    },
    {
        "name": "nairu_cosplay_reveal",
        "prompt": (
            "A dramatic slow-motion reveal of a beautiful woman with straight black "
            "hair in an elaborate anime-inspired cosplay outfit. Purple and blue "
            "lighting creates a dramatic atmosphere. She strikes a confident pose "
            "and the camera orbits around her. Cinematic, high-fashion editorial "
            "style, photorealistic, dramatic shadows."
        ),
        "reference_image": "gallery3.png",
        "aspect_ratio": "16:9",   # Landscape for YouTube/promo
        "duration": 5,
    },
    {
        "name": "nairu_lifestyle",
        "prompt": (
            "A beautiful woman with long straight black hair in casual chic attire "
            "walks through a modern urban setting at golden hour. She looks back at "
            "the camera with a mysterious smile. Soft cinematic lighting, shallow "
            "depth of field, warm color palette with purple accents. Hair flowing "
            "gently in the breeze. Photorealistic, 4K."
        ),
        "reference_image": "gallery4.png",
        "aspect_ratio": "9:16",
        "duration": 5,
    },
]


def generate_video(prompt_config: dict):
    """Generate a single video using Veo 3.1."""
    name = prompt_config["name"]
    prompt = prompt_config["prompt"]
    aspect = prompt_config.get("aspect_ratio", "9:16")
    duration = prompt_config.get("duration", 5)
    ref_image_name = prompt_config.get("reference_image")

    print(f"\n🎬 Generating: {name}")
    print(f"   Prompt: {prompt[:80]}...")
    print(f"   Aspect: {aspect} | Duration: {duration}s")

    # Build config
    config_params = {
        "aspect_ratio": aspect,
        "person_generation": "allow_adult",
    }

    # Build kwargs
    kwargs = {
        "model": "veo-3.1-generate-preview",
        "prompt": prompt,
        "config": types.GenerateVideosConfig(**config_params),
    }

    # Add reference image if available
    if ref_image_name:
        ref_path = IMAGES_DIR / ref_image_name
        if ref_path.exists():
            print(f"   📸 Using reference image: {ref_image_name}")
            ref_image = load_image(str(ref_path))
            kwargs["config"] = types.GenerateVideosConfig(
                **config_params,
                reference_images=[
                    types.VideoGenerationReferenceImage(
                        image=ref_image,
                        reference_type="subject",
                    )
                ],
            )

    # Start generation
    print(f"   ⏳ Submitting to Veo 3.1...")
    try:
        operation = client.models.generate_videos(**kwargs)
    except Exception as e:
        print(f"   ❌ Error submitting: {e}")
        # Fallback: try without reference image
        print(f"   🔄 Retrying without reference image...")
        kwargs.pop("config", None)
        kwargs["config"] = types.GenerateVideosConfig(
            aspect_ratio=aspect,
            person_generation="allow_adult",
        )
        try:
            operation = client.models.generate_videos(**kwargs)
        except Exception as e2:
            print(f"   ❌ Fallback also failed: {e2}")
            return None

    # Poll for completion
    elapsed = 0
    while not operation.done:
        print(f"   ⏳ Waiting... ({elapsed}s elapsed)")
        time.sleep(15)
        elapsed += 15
        operation = client.operations.get(operation)
        if elapsed > 600:  # 10 min timeout
            print(f"   ⚠️ Timeout after {elapsed}s")
            return None

    # Download result
    output_path = OUTPUT_DIR / f"{name}.mp4"
    try:
        video = operation.response.generated_videos[0]
        client.files.download(file=video.video)
        video.video.save(str(output_path))
        print(f"   ✅ Saved: {output_path}")
        return output_path
    except Exception as e:
        print(f"   ❌ Error downloading: {e}")
        return None


def main():
    print("=" * 60)
    print("🎥 Nairu AI Video Generator — Veo 3.1")
    print("=" * 60)
    print(f"📁 Output: {OUTPUT_DIR}")
    print(f"📸 Reference images: {IMAGES_DIR}")
    print(f"🔑 API Key: {GEMINI_API_KEY[:12]}...{GEMINI_API_KEY[-4:]}")
    print(f"🎬 Videos to generate: {len(VIDEO_PROMPTS)}")
    print("=" * 60)

    results = []
    for i, prompt_config in enumerate(VIDEO_PROMPTS, 1):
        print(f"\n[{i}/{len(VIDEO_PROMPTS)}]", end="")
        result = generate_video(prompt_config)
        results.append((prompt_config["name"], result))

    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    for name, path in results:
        status = f"✅ {path}" if path else "❌ Failed"
        print(f"  {name}: {status}")

    successful = sum(1 for _, p in results if p)
    print(f"\n🎉 {successful}/{len(results)} videos generated successfully!")
    print(f"📁 Files saved in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
