"""
Nairu AI Video Generator — Batch 20+ Videos
Uses Veo 3.1 via Gemini API with CONSISTENT face reference (hero.png)
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
# 20 VIDEO PROMPTS
# ============================================================
# Category: TEASER (3) — more clothed, gamer/otaku aesthetic
# Category: VIP SENSUAL (10) — cosplay, lingerie, alluring poses
# Category: VIP HOT (7) — provocative anime-inspired, body focused
# ============================================================

VIDEO_PROMPTS = [
    # ---- TEASER (3 vídeos — para feed/preview) ----
    {
        "name": "teaser_gamer_girl",
        "prompt": NAIRU_DESC + (
            "She sits cross-legged on a gaming chair wearing a short oversized "
            "purple gamer t-shirt dress that reveals her legs, with a RGB gaming "
            "headset around her neck. She picks up the headset, puts it on, and "
            "winks at camera with a playful smile. Purple and pink neon gaming "
            "room background. Cinematic, warm lighting, photorealistic 4K."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "teaser_otaku_morning",
        "prompt": NAIRU_DESC + (
            "She wears a short silk nightgown with anime prints, standing by a "
            "window in soft golden morning light. She stretches her arms above "
            "her head, yawning cutely, then looks at the camera and smiles. "
            "Cozy bedroom with anime posters on the wall. Her hair flows softly. "
            "Cinematic, dreamy atmosphere, shallow depth of field, photorealistic."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "teaser_cosplay_prep",
        "prompt": NAIRU_DESC + (
            "She sits at a vanity mirror applying makeup for cosplay, wearing a "
            "tank top. She turns to camera and blows a kiss with a confident look. "
            "RGB lights and anime figurines visible in background. Close-up to "
            "medium shot, cinematic lighting with purple and blue tones, "
            "photorealistic, beautiful skin detail."
        ),
        "aspect_ratio": "9:16",
    },

    # ---- VIP SENSUAL COSPLAY (10 vídeos) ----
    {
        "name": "vip_bunny_cosplay",
        "prompt": NAIRU_DESC + (
            "She wears a sleek black bunny girl bodysuit cosplay with sheer "
            "stockings and bunny ears headband. She poses confidently, turning "
            "slowly to show the outfit from different angles. Dark studio with "
            "dramatic purple spotlight. Fashion editorial style, cinematic "
            "lighting, slow motion hair movement, photorealistic 4K."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "vip_maid_cosplay",
        "prompt": NAIRU_DESC + (
            "She wears a short French maid cosplay outfit with frills and "
            "thigh-high stockings. She curtsies playfully, then tilts her head "
            "with a sweet smile. Cherry blossom petals fall around her. Soft "
            "pink and purple lighting, anime-inspired atmosphere, cinematic, "
            "photorealistic, shallow depth of field."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "vip_catgirl_cosplay",
        "prompt": NAIRU_DESC + (
            "She wears a black cat-ear headband, choker, and a fitted black "
            "bodysuit with a tail. She does a cat paw pose with both hands, "
            "playfully meowing at the camera. Neon-lit bedroom with purple "
            "ambient lighting. Cute and alluring, close-up shot, cinematic, "
            "photorealistic, beautiful eyes detail."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "vip_succubus_cosplay",
        "prompt": NAIRU_DESC + (
            "She wears a dark purple succubus cosplay with small horns headband "
            "and a black corset. She gazes intensely at the camera with a "
            "seductive half-smile, slowly running her fingers through her hair. "
            "Dark moody background with red and purple smoke effects. Dramatic "
            "cinematic lighting, editorial fashion, photorealistic 4K."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "vip_schoolgirl_cosplay",
        "prompt": NAIRU_DESC + (
            "She wears a Japanese schoolgirl uniform cosplay (short plaid skirt, "
            "white blouse, loose tie). She sits on a desk, crossing her legs, "
            "looking at the camera over her shoulder with a playful expression. "
            "Classroom setting with cherry blossom visible through window. "
            "Anime aesthetic, soft lighting, photorealistic, cinematic."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "vip_nurse_cosplay",
        "prompt": NAIRU_DESC + (
            "She wears a short nurse cosplay outfit with a small cap, holding "
            "a stethoscope. She leans forward slightly and puts a finger to "
            "her lips in a shush gesture, smiling mischievously. Clean white "
            "background with soft pink lighting accents. Fashion editorial, "
            "cinematic, photorealistic, attractive pose."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "vip_witch_cosplay",
        "prompt": NAIRU_DESC + (
            "She wears a sexy witch cosplay with a pointed hat, short black "
            "dress and thigh-high boots. She twirls a wand playfully, casting "
            "sparkle effects. Mystical dark forest backdrop with floating "
            "magical lights. Fantasy cinematic style, purple and gold color "
            "grading, photorealistic, enchanting atmosphere."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "vip_pool_bikini",
        "prompt": NAIRU_DESC + (
            "She wears a small purple string bikini, standing by a luxurious "
            "infinity pool at sunset. She walks slowly towards camera, hair "
            "flowing in the breeze, with a confident sultry walk. Golden hour "
            "lighting, tropical paradise background, cinematic slow motion, "
            "photorealistic 4K, fashion campaign style."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "vip_lingerie_boudoir",
        "prompt": NAIRU_DESC + (
            "She reclines on a luxurious bed in elegant black lace lingerie, "
            "propped on her elbow, looking at the camera with a sultry gaze. "
            "Soft boudoir lighting with purple and warm tones, silk sheets, "
            "candles in background. Fashion editorial boudoir style, "
            "cinematic, photorealistic, intimate atmosphere."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "vip_latex_cosplay",
        "prompt": NAIRU_DESC + (
            "She wears a glossy dark purple latex bodysuit in a futuristic "
            "cyberpunk setting. She stands with hands on hips in a power pose, "
            "then slowly turns. Neon signs and holographic elements in background. "
            "Blade Runner aesthetic, dramatic lighting with blue and purple, "
            "photorealistic 4K, sci-fi fashion editorial."
        ),
        "aspect_ratio": "9:16",
    },

    # ---- VIP HOT ANIME-INSPIRED (7 vídeos) ----
    {
        "name": "vip_anime_pose_1",
        "prompt": NAIRU_DESC + (
            "She wears a revealing red and black anime warrior cosplay with "
            "armor accents. She draws a katana slowly and strikes a dramatic "
            "battle pose. Wind blows her hair dynamically. Cherry blossom "
            "petals swirl around her. Epic anime-inspired cinematography, "
            "dramatic lighting, photorealistic 4K, action figure aesthetic."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "vip_anime_pose_2",
        "prompt": NAIRU_DESC + (
            "She wears a form-fitting white and blue sailor moon inspired "
            "cosplay. She does the iconic moon transformation pose, spinning "
            "gracefully. Magical sparkle effects surround her. Dramatic anime "
            "lighting with stars and moonlight, photorealistic rendering, "
            "cinematic slow motion, dreamy atmosphere."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "vip_anime_pose_3",
        "prompt": NAIRU_DESC + (
            "She wears a black and purple skin-tight battle suit inspired by "
            "anime. She crouches in a dynamic action pose, looking up at the "
            "camera with fierce determination. Rain drops frozen in mid-air. "
            "Dark urban rooftop at night, neon city lights below. Dramatic "
            "cinematic lighting, photorealistic, intense atmosphere."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "vip_anime_pose_4",
        "prompt": NAIRU_DESC + (
            "She wears a Japanese shrine maiden (miko) cosplay with a short "
            "white top and red hakama skirt. She holds a ceremonial bow, "
            "standing at a torii gate. Cherry blossoms fall around her as she "
            "turns to camera with a serene smile. Golden hour lighting, "
            "spiritual atmosphere, photorealistic, cinematic."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "vip_anime_pose_5",
        "prompt": NAIRU_DESC + (
            "She wears a close-fitting dark EVA-inspired plugsuit cosplay. "
            "She sits in a dramatic pose with one knee up, looking at camera "
            "with an intense gaze. Control room with holographic screens behind "
            "her. Dramatic blue and orange lighting, sci-fi atmosphere, "
            "photorealistic 4K, cinematic composition."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "vip_anime_pose_6",
        "prompt": NAIRU_DESC + (
            "She wears a Boa Hancock-inspired pirate empress cosplay with a "
            "long flowing cape and ornate jewelry. She stands regally with a "
            "confident smirk, tossing her long black hair back. Ocean and "
            "pirate ship in background. Dramatic sunset lighting, epic "
            "cinematic style, photorealistic, powerful feminine energy."
        ),
        "aspect_ratio": "16:9",
    },
    {
        "name": "vip_anime_pose_7",
        "prompt": NAIRU_DESC + (
            "She wears a Zero Two-inspired pink and red bodysuit cosplay with "
            "small horns. She leans forward toward the camera, reaching out "
            "with one hand, with a playful and alluring expression. Pink "
            "cherry blossom background, soft romantic lighting, bokeh effects, "
            "photorealistic 4K, anime-inspired cinematic style."
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
        print(f"\n   ✅ {output_path.name} ({output_path.stat().st_size / 1024 / 1024:.1f}MB)")
        return output_path
    except Exception as e:
        print(f"\n   ❌ Download error: {e}")
        return None


def main():
    total = len(VIDEO_PROMPTS)
    print("=" * 60)
    print(f"🎥 Nairu Batch Video Generator — {total} videos")
    print(f"📸 Face ref: {FACE_REF}")
    print(f"📁 Output: {OUTPUT_DIR}")
    print("=" * 60)

    results = []
    for i, cfg in enumerate(VIDEO_PROMPTS, 1):
        result = generate_video(cfg, i, total)
        results.append((cfg["name"], result))

    # Summary
    ok = sum(1 for _, r in results if r)
    print(f"\n{'=' * 60}")
    print(f"📊 {ok}/{total} generated")
    for name, r in results:
        s = "✅" if r else "❌"
        print(f"  {s} {name}")
    print(f"📁 {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
