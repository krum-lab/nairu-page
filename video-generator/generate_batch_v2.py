"""
Nairu AI Video Generator — Batch V2: 15 New Videos
Uses Veo 3.1 via Gemini API with CONSISTENT face reference (hero.png)
Focus: More SFW teasers, tasteful cosplay, lifestyle — optimized for monetization
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / "telegram-bot" / ".env"
load_dotenv(env_path)

from google import genai
from google.genai import types

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY not found"); sys.exit(1)

client = genai.Client(api_key=GEMINI_API_KEY)

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

IMAGES_DIR = Path(__file__).parent.parent / "landing-page" / "assets" / "images"

# Primary face reference — used in ALL videos for consistency
FACE_REF = IMAGES_DIR / "hero.png"

# Physical description prefix — appended to all prompts for consistency
NAIRU_DESC = (
    "The subject is a beautiful Brazilian woman, 28 years old, with long straight "
    "jet-black hair, fair light skin, warm brown eyes, soft facial features, "
    "slim athletic body with feminine curves, no freckles. "
)


def load_image(path: Path) -> types.Image:
    with open(path, "rb") as f:
        return types.Image(image_bytes=f.read(), mime_type="image/png")


# ============================================================
# 15 NEW VIDEO PROMPTS — V2 BATCH
# ============================================================
# Category: REELS/TIKTOK (5) — SFW, viral, short-form optimized
# Category: COSPLAY VIP (5) — tasteful cosplay for monetization
# Category: LIFESTYLE (5) — casual, relatable, behind-the-scenes
# ============================================================

VIDEO_PROMPTS = [
    # ---- REELS/TIKTOK (5 vídeos — SFW, viral potential) ----
    {
        "name": "reel_anime_dance",
        "prompt": NAIRU_DESC + (
            "She stands in a stylish gaming room with RGB neon lights, wearing a "
            "cute oversized anime t-shirt and black shorts. She does a trending "
            "TikTok dance with smooth choreography, smiling and having fun. The "
            "camera is static, front-facing, phone selfie angle. Purple and pink "
            "ambient lighting, energetic mood, photorealistic 4K, vertical video."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "reel_outfit_transition",
        "prompt": NAIRU_DESC + (
            "Fashion transition video. She starts wearing a casual oversized "
            "hoodie in her bedroom, then snaps her fingers — cut to her wearing "
            "a stylish black crop top and fitted jeans, hair perfectly styled. "
            "She does a confident pose and winks at camera. Before/after magic "
            "transition effect. Purple neon bedroom, photorealistic, TikTok style."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "reel_gaming_reaction",
        "prompt": NAIRU_DESC + (
            "Close-up of her sitting in a gaming chair wearing a headset. She is "
            "intensely focused on gaming, then suddenly celebrates a victory with "
            "an excited fist pump and a big genuine smile. The screen's RGB light "
            "reflects on her face. Gaming room background with monitors. "
            "Authentic reaction, cinematic close-up, photorealistic."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "reel_manga_asmr",
        "prompt": NAIRU_DESC + (
            "ASMR-style close-up video. She sits cross-legged on a cozy bed, "
            "wearing a soft oversized sweater, slowly flipping through manga "
            "pages. Soft ambient lighting, fairy lights in background. The camera "
            "focuses on her hands turning colorful manga pages, then pans up to "
            "her serene smiling face. Cozy atmosphere, soft sounds implied, "
            "cinematic shallow depth of field, photorealistic."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "reel_unboxing_figurine",
        "prompt": NAIRU_DESC + (
            "She excitedly unboxes an anime figurine, sitting at a desk in her "
            "gaming room. She opens the box, gasps with genuine excitement, and "
            "carefully lifts out the figurine, examining it with sparkling eyes. "
            "She holds it up to the camera proudly. Desk has anime posters behind "
            "her, RGB lighting. Fun, authentic energy, photorealistic, TikTok angle."
        ),
        "aspect_ratio": "9:16",
    },

    # ---- COSPLAY VIP (5 vídeos — tasteful, for monetization) ----
    {
        "name": "vip_chun_li_cosplay",
        "prompt": NAIRU_DESC + (
            "She wears a Chun-Li inspired cosplay with blue qipao dress and white "
            "boots. She performs Chun-Li's signature kick pose in slow motion, "
            "hair and outfit moving dynamically. Martial arts dojo background with "
            "soft golden lamplight. Power pose, confident expression. Cinematic "
            "action photography style, photorealistic 4K, dynamic composition."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "vip_dva_cosplay",
        "prompt": NAIRU_DESC + (
            "She wears a D.Va inspired bodysuit cosplay in pink and white, with "
            "whisker face paint. She makes a heart shape with her hands and "
            "does D.Va's iconic 'GG' pose, winking at the camera. Futuristic "
            "gaming background with holographic screens. Cute and confident. "
            "Neon pink and blue lighting, cinematic, photorealistic 4K."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "vip_2b_cosplay",
        "prompt": NAIRU_DESC + (
            "She wears a 2B (NieR Automata) inspired cosplay with short black "
            "gothic lolita dress and silver blindfold pushed up on forehead. She "
            "stands elegantly holding a katana, wind blowing her hair and dress. "
            "Desolate beautiful ruins background with flowers growing. Melancholic "
            "beauty, golden hour backlight, cinematic, photorealistic 4K."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "vip_misato_cosplay",
        "prompt": NAIRU_DESC + (
            "She wears a Misato Katsuragi inspired outfit: red leather jacket "
            "over a black dress, cross necklace. She leans against a railing "
            "on a city balcony at night, city lights bokeh behind her. She takes "
            "a sip from a coffee cup and looks at the camera with a confident "
            "smile. Urban night aesthetic, cinematic lighting, photorealistic."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "vip_rem_cosplay",
        "prompt": NAIRU_DESC + (
            "She wears a Rem (Re:Zero) inspired maid cosplay with blue details "
            "and headband. She gracefully curtsies in a cherry blossom garden, "
            "petals falling around her. She then looks up at the camera with a "
            "sweet gentle smile. Dreamy pink and white atmosphere, soft focus, "
            "romantic anime aesthetic, photorealistic 4K, fairy-tale mood."
        ),
        "aspect_ratio": "9:16",
    },

    # ---- LIFESTYLE / BTS (5 vídeos — casual, relatable) ----
    {
        "name": "life_coffee_morning",
        "prompt": NAIRU_DESC + (
            "Cozy morning routine video. She wears a silk pajama set, walks into "
            "a sunlit kitchen, makes coffee in a stylish mug. She wraps her hands "
            "around the warm mug and takes a sip, closing her eyes with a blissful "
            "smile. Morning sunshine through window, warm golden tones, lifestyle "
            "vlog style, slow motion, photorealistic, calming atmosphere."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "life_workout_gamer",
        "prompt": NAIRU_DESC + (
            "She wears a black sports bra and yoga pants in a modern home gym. "
            "She does stretching exercises, then sits down and puts on gaming "
            "headphones, transitioning from workout to gaming. Energetic but "
            "chill vibe. Natural lighting mixed with RGB accents. Active "
            "lifestyle content, cinematic, photorealistic."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "life_sunset_rooftop",
        "prompt": NAIRU_DESC + (
            "She stands on an urban rooftop at sunset wearing a stylish casual "
            "outfit: black fitted jeans and a cropped jacket. She gazes at the "
            "city skyline, then turns to the camera with a warm smile. Wind "
            "blows her hair softly. Golden hour cinematic lighting, city "
            "panorama, lifestyle photography, photorealistic 4K."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "life_night_neon",
        "prompt": NAIRU_DESC + (
            "She walks through a vibrant neon-lit Asian street market at night, "
            "wearing a trendy streetwear outfit. She looks at the colorful neon "
            "signs with wonder, then turns to camera with a playful smile. Rain "
            "glistens on the ground reflecting neon lights. Cyberpunk atmosphere, "
            "cinematic slow motion, blade runner color palette, photorealistic."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "life_reading_rainy",
        "prompt": NAIRU_DESC + (
            "She sits in a cozy window seat reading a book while rain falls "
            "outside. She wears a soft oversized knit sweater. A warm lamp casts "
            "golden light on her. She looks up from the book and smiles gently "
            "at the camera. Raindrops on the window glass create beautiful bokeh. "
            "Intimate, ASMR-like atmosphere, photorealistic, warm tones."
        ),
        "aspect_ratio": "9:16",
    },
]


def generate_video(prompt_config: dict, index: int, total: int):
    """Generate a single video with face reference for consistency."""
    name = prompt_config["name"]
    prompt = prompt_config["prompt"]
    aspect = prompt_config.get("aspect_ratio", "9:16")

    output_path = OUTPUT_DIR / f"{name}.mp4"

    # Skip if already exists
    if output_path.exists():
        print(f"\n[{index}/{total}] ⏭️  {name} — already exists, skipping")
        return output_path

    print(f"\n[{index}/{total}] 🎬 {name}")
    print(f"   Aspect: {aspect}")

    # Load face reference for consistency
    face_ref = load_image(FACE_REF)

    config = types.GenerateVideosConfig(
        aspect_ratio=aspect,
        person_generation="allow_adult",
        reference_images=[
            types.VideoGenerationReferenceImage(
                image=face_ref,
                reference_type="subject",
            )
        ],
    )

    print(f"   ⏳ Submitting to Veo 3.1 (with face reference)...")
    try:
        operation = client.models.generate_videos(
            model="veo-3.1-generate-preview",
            prompt=prompt,
            config=config,
        )
    except Exception as e:
        print(f"   ❌ Error: {e}")
        # Retry without reference
        print(f"   🔄 Retrying text-only...")
        try:
            config_fallback = types.GenerateVideosConfig(
                aspect_ratio=aspect,
                person_generation="allow_adult",
            )
            operation = client.models.generate_videos(
                model="veo-3.1-generate-preview",
                prompt=prompt,
                config=config_fallback,
            )
        except Exception as e2:
            print(f"   ❌ Failed: {e2}")
            return None

    # Poll
    elapsed = 0
    while not operation.done:
        print(f"   ⏳ {elapsed}s...", end="\r")
        time.sleep(15)
        elapsed += 15
        try:
            operation = client.operations.get(operation)
        except Exception:
            time.sleep(5)
            operation = client.operations.get(operation)
        if elapsed > 600:
            print(f"\n   ⚠️ Timeout"); return None

    # Download
    try:
        video = operation.response.generated_videos[0]
        client.files.download(file=video.video)
        video.video.save(str(output_path))
        size_mb = output_path.stat().st_size / 1024 / 1024
        print(f"\n   ✅ {output_path.name} ({size_mb:.1f}MB)")
        return output_path
    except Exception as e:
        print(f"\n   ❌ Download error: {e}")
        return None


def main():
    total = len(VIDEO_PROMPTS)
    print("=" * 60)
    print(f"🎥 Nairu Batch V2 — {total} new videos")
    print(f"📸 Face ref: {FACE_REF}")
    print(f"📁 Output: {OUTPUT_DIR}")
    print("=" * 60)

    if not FACE_REF.exists():
        print(f"❌ Face reference not found: {FACE_REF}")
        sys.exit(1)

    results = []
    for i, cfg in enumerate(VIDEO_PROMPTS, 1):
        result = generate_video(cfg, i, total)
        results.append((cfg["name"], result))

        # Brief pause between requests to be kind to the API
        if result and i < total:
            time.sleep(5)

    # Summary
    ok = sum(1 for _, r in results if r)
    print(f"\n{'=' * 60}")
    print(f"📊 Results: {ok}/{total} generated")
    for name, r in results:
        s = "✅" if r else "❌"
        print(f"  {s} {name}")
    print(f"📁 {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
