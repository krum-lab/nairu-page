"""
Nairu AI Video Generator — Batch V2: 15 Videos with PT-BR Voice + Extension
Uses Veo 3.1 via Gemini API with face reference (hero.png)
Voice: Brazilian Portuguese with São Paulo accent
Duration: 15 seconds (8s base + 7s extension)
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

# Primary face reference
FACE_REF = IMAGES_DIR / "hero.png"

# Physical description + voice instruction in ALL prompts
NAIRU_DESC = (
    "The subject is a beautiful Brazilian woman, 28 years old, with long straight "
    "jet-black hair, fair light skin, warm brown eyes, soft facial features, "
    "slim athletic body with feminine curves, no freckles. "
    "She speaks in Brazilian Portuguese with a São Paulo accent, "
    "her voice is warm, playful, flirty, and naturally charming with a "
    "youthful energy. She uses Brazilian expressions and slang naturally. "
)

# Audio atmosphere prefix — ensures Veo generates rich audio
AUDIO_PREFIX = (
    "The video has rich, immersive audio throughout: "
)


def load_image(path: Path) -> types.Image:
    with open(path, "rb") as f:
        return types.Image(image_bytes=f.read(), mime_type="image/png")


# ============================================================
# 15 VIDEO PROMPTS — V2 with PT-BR voice + engaging audio
# All prompts describe continuous action for 15+ seconds
# ============================================================

VIDEO_PROMPTS = [
    # ---- REELS/TIKTOK (5) ----
    {
        "name": "reel_anime_dance",
        "prompt": NAIRU_DESC + AUDIO_PREFIX + (
            "ambient music plays softly, her clothing rustles as she moves. "
            "She stands in a stylish gaming room with RGB purple and pink neon lights, "
            "wearing a cute oversized anime t-shirt and black shorts. She looks at "
            "the camera and says cheerfully \"E aí gente, bora dançar? Essa opening "
            "é demais!\" She starts doing a fun anime-style dance, humming along "
            "to the rhythm. Midway she laughs and says \"Ai, errei o passo, gente! "
            "Mas tá valendo!\" She keeps dancing, spins around playfully, then "
            "strikes a cute pose at the end saying \"Segue aí pra mais!\" with a "
            "wink. Energetic mood, photorealistic 4K, vertical video."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "reel_outfit_transition",
        "prompt": NAIRU_DESC + AUDIO_PREFIX + (
            "bedroom ambient sounds, fabric rustling, dramatic whoosh effect on transition. "
            "Fashion transition video in her bedroom with purple neon lights. "
            "She starts wearing a casual oversized hoodie, yawning and saying "
            "\"Bom dia, tô um bagulho agora... mas olha só a transformação\" She "
            "counts down \"Três... dois... um!\" and snaps her fingers — dramatic "
            "transition cut to her wearing a stylish black crop top and fitted jeans, "
            "hair perfectly styled. She says \"Olha isso, hein? De randomzinha pra "
            "pronta pra sair em três segundos\" She does a slow turn showing the "
            "outfit, then says \"Gostaram? Comenta aí qual look vocês preferem\" "
            "with a confident wink. Photorealistic, TikTok style."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "reel_gaming_reaction",
        "prompt": NAIRU_DESC + AUDIO_PREFIX + (
            "intense game sound effects, keyboard clicking, mouse clicking, victory fanfare. "
            "Close-up of her in a gaming chair wearing a headset in her RGB gaming room. "
            "She's intensely focused on gaming, breathing nervously and muttering "
            "\"Vai, vai, vai... pelo amor de Deus, não morre...\" She leans forward, "
            "keyboard sounds intensify, then she suddenly screams \"VAMO CARAMBA! "
            "GANHEI! Mano, que clutch insano!\" She throws her fist up in excitement, "
            "then leans back laughing \"Gente, minhas mãos tão tremendo, olha\" She "
            "shows her shaking hands to the camera, still giggling. \"Quem joga "
            "comigo? Deixa nos comentários\" The RGB lights pulse with her excitement. "
            "Authentic reaction, cinematic, photorealistic."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "reel_manga_asmr",
        "prompt": NAIRU_DESC + AUDIO_PREFIX + (
            "soft ASMR page-turning sounds, gentle paper crinkling, quiet ambient rain outside. "
            "ASMR-style close-up. She sits cross-legged on a cozy bed with "
            "fairy lights in the background, wearing a soft oversized sweater, "
            "slowly flipping through colorful manga pages. She whispers softly "
            "\"Gente, vocês já leram esse capítulo? É insano\" She turns another "
            "page carefully, the paper crinkling sound is satisfying. She gasps "
            "quietly \"Ai meu Deus, o que o autor fez aqui...\" She giggles "
            "softly and hugs the manga to her chest saying \"Não vou dar spoiler "
            "mas... preparem o coração\" She looks at camera with big warm eyes "
            "and smiles. Cozy ASMR atmosphere, photorealistic, warm lighting."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "reel_unboxing_figurine",
        "prompt": NAIRU_DESC + AUDIO_PREFIX + (
            "cardboard box opening sounds, bubble wrap popping, excited gasps. "
            "She's at her gaming desk surrounded by anime posters and RGB lights. "
            "She holds a delivery box and says excitedly \"Olha o que chegou, "
            "gente! Eu tô morrendo de ansiedade\" She carefully opens the box, "
            "bubble wrap sounds, then she peels back the packaging and gasps "
            "\"Ai meu Deus, que LINDA! Olha o detalhe, gente\" She carefully "
            "lifts out an anime figurine, turning it around in her hands saying "
            "\"A pintura, a pose, tudo perfeito\" She places it on her shelf "
            "next to others and says \"Minha coleção tá crescendo demais, já "
            "não cabe mais nada aqui\" She laughs. Authentic unboxing energy, "
            "photorealistic, TikTok angle."
        ),
        "aspect_ratio": "9:16",
    },

    # ---- COSPLAY VIP (5) ----
    {
        "name": "vip_chun_li_cosplay",
        "prompt": NAIRU_DESC + AUDIO_PREFIX + (
            "martial arts whoosh sounds, fabric movement, confident footsteps. "
            "She wears a Chun-Li inspired cosplay with blue qipao dress and white "
            "boots in a martial arts dojo with warm golden lamplight. She walks "
            "toward camera confidently and says \"Chun-Li representando, galera!\" "
            "She performs the signature spinning kick in slow motion with dramatic "
            "whoosh sounds, hair and outfit flowing dynamically. She wobbles "
            "slightly and laughs \"Quase caí gente, cosplay não é fácil\" She "
            "strikes the victory pose and says \"Mas ficou lindo, né? Comenta "
            "qual cosplay vocês querem ver\" Then winks. Cinematic action style, "
            "photorealistic 4K."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "vip_dva_cosplay",
        "prompt": NAIRU_DESC + AUDIO_PREFIX + (
            "futuristic beeps, gaming sound effects, cute voice. "
            "She wears a D.Va inspired bodysuit cosplay in pink and white, with "
            "whisker face paint, in a futuristic room with holographic screens. "
            "She makes a heart shape with her hands saying \"GG fácil, né amor?\" "
            "She does D.Va's iconic pose and says \"Quem aí joga Overwatch comigo? "
            "Preciso de um duo\" She pretends to press buttons in the air while "
            "making game sound effects \"Pew pew pew\" then laughs \"Tô zoando\" "
            "She leans toward camera and whispers \"Mas os cosplays VIP tão ficando "
            "cada vez melhores, hein\" Winks. Neon pink and blue lighting, "
            "cinematic, photorealistic 4K."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "vip_2b_cosplay",
        "prompt": NAIRU_DESC + AUDIO_PREFIX + (
            "wind blowing, blade unsheathing sound, ethereal ambient music. "
            "She wears a 2B (NieR Automata) inspired cosplay with short black "
            "gothic lolita dress and silver blindfold pushed up. She stands in "
            "beautiful desolate ruins with flowers growing, golden hour backlight. "
            "Wind blows her hair dramatically. She draws a katana slowly with a "
            "metallic sound, saying softly \"Glória à humanidade...\" She holds "
            "the pose for a moment, then breaks character and smiles saying \"NieR "
            "Automata é o melhor jogo de todos os tempos, aceito brigas\" She "
            "sheathes the katana, looks at camera with mysterious eyes and says "
            "\"Vocês jogaram? Me conta\" Cinematic, photorealistic 4K."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "vip_misato_cosplay",
        "prompt": NAIRU_DESC + AUDIO_PREFIX + (
            "city ambient sounds at night, coffee cup clink, evening breeze. "
            "She wears Misato Katsuragi outfit: red leather jacket, black dress, "
            "cross necklace. She leans on a city balcony railing at night with "
            "bokeh city lights behind her. She takes a sip of coffee, sighs "
            "contentedly and says \"Evangelion é cultura, né gente? Nunca superei "
            "o final\" She looks at the city lights contemplatively, then turns "
            "to camera with a smirk \"Quem aí é team Misato? Levanta a mão\" "
            "She raises her coffee cup and says \"Saúde! Ou como a Misato diria... "
            "kampai!\" She laughs warmly. Urban night aesthetic, cinematic, "
            "photorealistic."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "vip_rem_cosplay",
        "prompt": NAIRU_DESC + AUDIO_PREFIX + (
            "gentle breeze, cherry blossom petals rustling, soft delicate footsteps. "
            "She wears Rem (Re:Zero) maid cosplay with blue details and headband "
            "in a cherry blossom garden. Petals fall around her gracefully. She "
            "curtsies elegantly and says sweetly \"Rem está aqui pra cuidar de "
            "você, tá?\" She walks slowly through the garden, touching blossoms "
            "gently. She looks at camera with soft eyes and says \"Esse cosplay "
            "me faz sentir tão fofa, gente\" She giggles and spins once, dress "
            "flowing, then says \"Re:Zero é a minha vida, quem concorda?\" She "
            "blows a kiss toward camera. Dreamy romantic atmosphere, "
            "photorealistic 4K."
        ),
        "aspect_ratio": "9:16",
    },

    # ---- LIFESTYLE (5) ----
    {
        "name": "life_coffee_morning",
        "prompt": NAIRU_DESC + AUDIO_PREFIX + (
            "coffee machine gurgling, birds chirping, morning city ambiance. "
            "Cozy morning routine. She wears silk pajamas and walks into a sunlit "
            "kitchen yawning \"Bom dia, amores\" She makes coffee — the machine "
            "gurgles, she hums softly while waiting. She pours and wraps her "
            "hands around the mug, takes a sip. Closes her eyes saying \"Hmm... "
            "café da manhã perfeito\" She opens her eyes and says to camera "
            "\"Sem café eu não funciono, vocês também são assim?\" She laughs and "
            "takes another sip \"Hoje o plano é: café, anime, e mais café\" She "
            "smiles warmly. Golden morning light, lifestyle vlog, photorealistic."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "life_workout_gamer",
        "prompt": NAIRU_DESC + AUDIO_PREFIX + (
            "workout music beat, exercise mat sounds, headphone click. "
            "She wears a black sports bra and yoga pants in a modern home gym. "
            "She finishes the last rep of crunches and sits up saying \"Ufa, "
            "treino feito!\" She catches her breath, then smiles \"Agora a melhor "
            "parte\" She walks over to her gaming setup and puts on headphones, "
            "clicking them on with a satisfying click. She says \"Treino pro corpo, "
            "game pra cabeça. Equilíbrio perfeito, né?\" She grabs the controller "
            "and says \"Prioridades, gente\" with a wink as she starts gaming. "
            "Natural lighting with RGB accents, cinematic, photorealistic."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "life_sunset_rooftop",
        "prompt": NAIRU_DESC + AUDIO_PREFIX + (
            "gentle wind, distant city traffic, atmospheric ambient music. "
            "She stands on an urban rooftop at golden hour sunset wearing black "
            "fitted jeans and cropped jacket. Wind blows her hair softly. She "
            "gazes at the city skyline in silence for a moment, then turns to "
            "camera saying \"São Paulo é linda assim, ó... olha esse pôr do sol\" "
            "She gestures at the skyline. \"Às vezes eu paro pra apreciar, sabe? "
            "A correria do dia a dia faz a gente esquecer\" She smiles warmly "
            "and says \"Aproveitem o momento, tá? Beijo\" She blows a kiss toward "
            "the sunset. Golden hour cinematic, city panorama, photorealistic 4K."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "life_night_neon",
        "prompt": NAIRU_DESC + AUDIO_PREFIX + (
            "city night sounds, rain on pavement, neon buzzing, footsteps on wet ground. "
            "She walks through a vibrant neon-lit Asian-style street at night in "
            "trendy streetwear. Neon signs reflect on wet pavement. She looks up "
            "at the colorful signs saying \"Que vibe esse lugar, gente\" She turns "
            "to camera with excitement \"Parece que a gente tá no Blade Runner, "
            "né?\" She walks further, the neon lights painting colors on her face. "
            "She beckons to camera saying \"Vem comigo, vou mostrar mais\" She "
            "laughs \"Eu poderia ficar aqui a noite inteira\" Rain starts drizzling. "
            "Cyberpunk atmosphere, cinematic slow motion, photorealistic."
        ),
        "aspect_ratio": "9:16",
    },
    {
        "name": "life_reading_rainy",
        "prompt": NAIRU_DESC + AUDIO_PREFIX + (
            "rain pattering on window glass, gentle thunder in distance, pages turning softly. "
            "She sits in a cozy window seat reading a book while rain falls outside. "
            "Wearing a soft oversized knit sweater. A warm lamp casts golden light. "
            "Rain patters steadily on the glass. She reads quietly, then looks up "
            "and says softly \"Dia de chuva é dia de ficar de boas, né?\" She "
            "sighs contentedly. \"Tô lendo um livro incrível, depois conto pra "
            "vocês\" She holds up the book briefly, then settles back. She looks "
            "at the rain on the window and says \"Eu amo esse som de chuva... dá "
            "um sono\" She yawns cutely and smiles. Intimate ASMR atmosphere, "
            "photorealistic, warm tones."
        ),
        "aspect_ratio": "9:16",
    },
]


def generate_video(prompt_config: dict, index: int, total: int):
    """Generate a single video with face reference and 8s duration."""
    name = prompt_config["name"]
    prompt = prompt_config["prompt"]
    aspect = prompt_config.get("aspect_ratio", "9:16")

    output_path = OUTPUT_DIR / f"{name}.mp4"

    # Skip if already exists
    if output_path.exists():
        print(f"\n[{index}/{total}] ⏭️  {name} — already exists, skipping")
        return output_path

    print(f"\n[{index}/{total}] 🎬 {name}")
    print(f"   Aspect: {aspect} | Duration: 8s base")

    # Load face reference
    face_ref = load_image(FACE_REF)

    config = types.GenerateVideosConfig(
        aspect_ratio=aspect,
        person_generation="allow_adult",
        number_of_videos=1,
        duration_seconds=8,
        reference_images=[
            types.VideoGenerationReferenceImage(
                image=face_ref,
                reference_type="subject",
            )
        ],
    )

    print(f"   ⏳ Submitting to Veo 3.1 (PT-BR voice + 8s)...")
    try:
        operation = client.models.generate_videos(
            model="veo-3.1-generate-preview",
            prompt=prompt,
            config=config,
        )
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print(f"   🔄 Retrying text-only...")
        try:
            config_fallback = types.GenerateVideosConfig(
                aspect_ratio=aspect,
                person_generation="allow_adult",
                duration_seconds=8,
            )
            operation = client.models.generate_videos(
                model="veo-3.1-generate-preview",
                prompt=prompt,
                config=config_fallback,
            )
        except Exception as e2:
            print(f"   ❌ Failed: {e2}")
            return None

    # Poll for completion
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

    # Download base video
    try:
        video = operation.response.generated_videos[0]
        client.files.download(file=video.video)
        video.video.save(str(output_path))
        size_mb = output_path.stat().st_size / 1024 / 1024
        print(f"\n   ✅ Base: {output_path.name} ({size_mb:.1f}MB)")
    except Exception as e:
        print(f"\n   ❌ Download error: {e}")
        return None

    # ---- EXTEND to 15 seconds (+7s) ----
    print(f"   🔄 Extending +7s to reach 15s total...")
    try:
        extend_operation = client.models.generate_videos(
            model="veo-3.1-generate-preview",
            video=video.video,  # top-level param, must be from previous generation
            prompt=prompt,
            config=types.GenerateVideosConfig(
                number_of_videos=1,
                resolution="720p",
            ),
        )

        # Poll extension
        elapsed = 0
        while not extend_operation.done:
            print(f"   ⏳ ext {elapsed}s...", end="\r")
            time.sleep(15)
            elapsed += 15
            try:
                extend_operation = client.operations.get(extend_operation)
            except Exception:
                time.sleep(5)
                extend_operation = client.operations.get(extend_operation)
            if elapsed > 600:
                print(f"\n   ⚠️ Extension timeout — keeping 8s version")
                return output_path

        # Download extended version (overwrite)
        ext_video = extend_operation.response.generated_videos[0]
        client.files.download(file=ext_video.video)
        ext_video.video.save(str(output_path))
        size_mb = output_path.stat().st_size / 1024 / 1024
        print(f"\n   ✅ Extended: {output_path.name} ({size_mb:.1f}MB, ~15s)")

    except Exception as e:
        print(f"\n   ⚠️ Extension error: {e}")
        print(f"   📎 Keeping 8s version")

    return output_path


def main():
    total = len(VIDEO_PROMPTS)
    print("=" * 60)
    print(f"🎥 Nairu Batch V2 — {total} videos")
    print(f"🗣️  Voice: PT-BR, sotaque paulista")
    print(f"⏱️  Duration: 15s (8s + 7s extension)")
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
        if result and i < total:
            time.sleep(5)

    # Summary
    ok = sum(1 for _, r in results if r)
    print(f"\n{'=' * 60}")
    print(f"📊 Results: {ok}/{total} generated (15s with PT-BR voice)")
    for name, r in results:
        s = "✅" if r else "❌"
        print(f"  {s} {name}")
    print(f"📁 {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
