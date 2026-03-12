"""
Nairu Content Manager — Organize & Distribute Content
Catalogs all videos and images, generates captions, exports per platform.
"""

import os
import json
from pathlib import Path
from datetime import datetime

# Directories
PROJECT_DIR = Path(__file__).parent.parent
VIDEOS_DIR = PROJECT_DIR / "video-generator" / "output"
IMAGES_DIR = PROJECT_DIR / "instagram" / "content"
LANDING_IMAGES = PROJECT_DIR / "landing-page" / "assets" / "images"
LANDING_VIDEOS = PROJECT_DIR / "landing-page" / "assets" / "videos"
OUTPUT_FILE = Path(__file__).parent / "content_catalog.json"

# ============================================================
# CAPTION TEMPLATES — per platform
# ============================================================

HASHTAGS = {
    "instagram": (
        "#gamergirl #cosplay #anime #otaku #gamingsetup "
        "#cosplaybrasil #gamergirlbrasil #nerd #geek #animegirl "
        "#manga #gaming #ps5 #pcgaming #cosplayer"
    ),
    "tiktok": (
        "#gamergirl #cosplay #anime #otaku #fyp #foryou "
        "#trending #viral #cosplaygirl #gamer #nerd"
    ),
    "twitter": (
        "#gamergirl #cosplay #anime #gamingsetup #otaku"
    ),
    "telegram": "",
}

# Caption templates by video category
CAPTIONS = {
    # ---- Existing videos ----
    "teaser_gamer_girl": {
        "instagram": "Meu cantinho gamer 🎮💜\nQuem aí também joga de madrugada? 😏\n{tags}",
        "tiktok": "POV: o setup ficou pronto 🎮⚡ #gamergirl #gaming #setup",
        "twitter": "Setup novo, headset on 🎮💜 Quem joga comigo hoje?",
        "telegram": "🎮 Meu cantinho gamer tá pronto! Quem quer jogar comigo? 💜",
    },
    "teaser_otaku_morning": {
        "instagram": "Bom dia, otakuzinhos ☀️💜\nManhã preguiçosa = manhã perfeita ✨\n{tags}",
        "tiktok": "Bom dia otaku ☀️💜 #anime #cozy #morning #otaku",
        "twitter": "Bom dia! ☀️ Manhã de anime e preguiça 💜",
        "telegram": "☀️ Bom dia, amor! Manhã preguiçosa com anime 💜",
    },
    "teaser_cosplay_prep": {
        "instagram": "Getting ready pro cosplay 🎭✨\nAdivinhem qual personagem? 💜\n{tags}",
        "tiktok": "GRWM cosplay edition 🎭✨ #cosplay #grwm #anime",
        "twitter": "Getting ready pro cosplay de hoje 🎭💜 Qual personagem?",
        "telegram": "🎭 Me arrumando pro cosplay... adivinha qual? 💜",
    },
    "vip_maid_cosplay": {
        "instagram": "Maid service, alguém? 🖤✨\nLink na bio para conteúdo exclusivo 🔥\n{tags}",
        "tiktok": "Maid cosplay vibes 🖤✨ #maidcosplay #cosplay #anime",
        "twitter": "Maid cosplay day 🖤 Link na bio 💜",
        "telegram": "🖤 Maid service, amor? 😏 Esse e muito mais no VIP 💜",
    },
    "vip_pool_bikini": {
        "instagram": "Sunset vibes 🌅✨\nConteúdo exclusivo no link da bio 🔥\n{tags}",
        "tiktok": "Golden hour 🌅✨ #sunset #vibes #pool",
        "twitter": "Sunset mood 🌅💜",
        "telegram": "🌅 Sunset vibes... quer mais? VIP 💜",
    },
    "vip_latex_cosplay": {
        "instagram": "Cyberpunk mood 💜⚡\nFuturo é agora. Link na bio 🔗\n{tags}",
        "tiktok": "Cyberpunk cosplay ⚡ #cyberpunk #cosplay #futuristic",
        "twitter": "Future is now ⚡💜 #cyberpunk",
        "telegram": "⚡ Cyberpunk mode on. Mais no VIP 💜",
    },
    "vip_anime_pose_1": {
        "instagram": "Anime warrior mode ⚔️🔥\nQuem reconhece a referência? 💜\n{tags}",
        "tiktok": "Anime warrior cosplay ⚔️ #anime #cosplay #warrior",
        "twitter": "Warrior mode on ⚔️💜",
        "telegram": "⚔️ Modo guerreira ativado! Gostou? VIP tem mais 💜",
    },
    "nairu_gaming_intro": {
        "instagram": "Prazer, Nairu 🎮💜\nGamer, otaku e criadora de conteúdo ✨\n{tags}",
        "tiktok": "Prazer, Nairu 🎮💜 #introduction #gamergirl #newcreator",
        "twitter": "Oii! Sou a Nairu 🎮 Gamer e otaku 💜 Vem me conhecer!",
        "telegram": "🎮 Oii! Sou a Nairu! Prazer em te conhecer 💜",
    },
    "nairu_selfie_vlog": {
        "instagram": "Sending love 💋💜\n{tags}",
        "tiktok": "💋💜 #selfie #cute #love",
        "twitter": "💋💜",
        "telegram": "💋 Mandando um beijo especial pra você 💜",
    },
    "nairu_cosplay_reveal": {
        "instagram": "Cosplay reveal 🎭✨\nO que acharam? 💜\n{tags}",
        "tiktok": "Cosplay reveal ✨ #cosplay #reveal #anime",
        "twitter": "Cosplay reveal! 🎭 O que acharam? 💜",
        "telegram": "🎭 Reveal! Gostaram do cosplay? 💜",
    },

    # ---- V2 batch videos ----
    "reel_anime_dance": {
        "instagram": "Dance comigo! 💃💜\nQual anime opening vocês querem? ✨\n{tags}",
        "tiktok": "Dance with me 💃✨ #animedance #dance #trending #fyp",
        "twitter": "Dançando no setup 💃💜 Qual opening vocês querem?",
        "telegram": "💃 Dance time! Qual anime opening vocês preferem? 💜",
    },
    "reel_outfit_transition": {
        "instagram": "Glow up 🔥✨\nDe preguiçosa pra ready em 3... 2... 1! 💜\n{tags}",
        "tiktok": "Glow up transition ✨ #transition #glowup #fashion #fyp",
        "twitter": "Quick transition 🔥💜",
        "telegram": "✨ De preguiçosa a ready em 1 segundo! 💜",
    },
    "reel_gaming_reaction": {
        "instagram": "VICTORY! 🏆🎮\nEssa cara de quem ganhou a ranked 😤💜\n{tags}",
        "tiktok": "When you win the ranked match 🏆😤 #gaming #victory #gamergirl",
        "twitter": "VICTORY ROYALE 🏆🎮💜",
        "telegram": "🏆 GANHEI! Essa cara de vitória 😤💜",
    },
    "reel_manga_asmr": {
        "instagram": "Manga time 📚✨\nQual mangá vocês estão lendo? 💜\n{tags}",
        "tiktok": "Manga ASMR 📚✨ #manga #asmr #reading #cozy #otaku",
        "twitter": "Manga time 📚 Qual vocês estão lendo? 💜",
        "telegram": "📚 Tarde de mangá... qual vocês recomendam? 💜",
    },
    "reel_unboxing_figurine": {
        "instagram": "UNBOXING! 📦✨\nMinha coleção cresceu mais um pouco 😍💜\n{tags}",
        "tiktok": "Anime figurine unboxing 📦😍 #unboxing #anime #figurine #collection",
        "twitter": "Nova figure! 📦😍 Minha coleção não para de crescer 💜",
        "telegram": "📦 Unboxing de figure! Amei demais 😍💜",
    },
    "vip_chun_li_cosplay": {
        "instagram": "YATTA! 🥋💜\nChun-Li cosplay check ✨ Link na bio 🔥\n{tags}",
        "tiktok": "Chun-Li cosplay 🥋✨ #chunli #streetfighter #cosplay",
        "twitter": "Chun-Li reporting for duty 🥋💜",
        "telegram": "🥋 Chun-Li mode! Gostou? Tem mais no VIP 💜",
    },
    "vip_dva_cosplay": {
        "instagram": "GG! 🎮💗\nD.Va cosplay = melhor cosplay 💜\nLink na bio 🔥\n{tags}",
        "tiktok": "D.Va GG 🎮💗 #dva #overwatch #cosplay #gamer",
        "twitter": "Nerf this! 🎮💗 D.Va cosplay 💜",
        "telegram": "🎮 GG! D.Va is here 💗 Mais cosplays no VIP 💜",
    },
    "vip_2b_cosplay": {
        "instagram": "Glory to mankind ⚔️🖤\n2B cosplay vibes ✨ Link na bio 🔥\n{tags}",
        "tiktok": "2B NieR Automata cosplay ⚔️🖤 #2b #nierautomata #cosplay",
        "twitter": "Glory to mankind ⚔️🖤 2B cosplay 💜",
        "telegram": "⚔️ 2B reporting... Glory to mankind 🖤💜",
    },
    "vip_misato_cosplay": {
        "instagram": "Misato vibes 🍺💜\nEvangelion forever ✨ Link na bio 🔥\n{tags}",
        "tiktok": "Misato Katsuragi cosplay 🍺💜 #evangelion #misato #cosplay",
        "twitter": "Misato mood tonight 🍺💜 #Evangelion",
        "telegram": "🍺 Misato vibes... cheers! 💜 Mais no VIP",
    },
    "vip_rem_cosplay": {
        "instagram": "Rem quer cuidar de você 💙✨\nLink na bio pro conteúdo completo 🔥\n{tags}",
        "tiktok": "Rem Re:Zero cosplay 💙✨ #rem #rezero #cosplay #anime",
        "twitter": "Rem is here 💙✨ #ReZero",
        "telegram": "💙 Rem quer cuidar de você... VIP para ver mais 💜",
    },
    "life_coffee_morning": {
        "instagram": "Primeira coisa da manhã ☕✨\nCafé e depois anime 💜\n{tags}",
        "tiktok": "Morning coffee routine ☕✨ #morningroutine #coffee #cozy",
        "twitter": "Café da manhã ☕💜 Depois? Anime.",
        "telegram": "☕ Bom dia! Café pronto, dia perfeito 💜",
    },
    "life_workout_gamer": {
        "instagram": "Treino + gaming = equilíbrio perfeito 💪🎮\n{tags}",
        "tiktok": "Workout to gaming pipeline 💪🎮 #workout #gaming #lifestyle",
        "twitter": "Treino feito, agora bora jogar 💪🎮💜",
        "telegram": "💪 Treino pronto! Agora modo gamer on 🎮💜",
    },
    "life_sunset_rooftop": {
        "instagram": "Sunset thoughts 🌅💜\nA vida é bonita demais ✨\n{tags}",
        "tiktok": "Rooftop sunset vibes 🌅✨ #sunset #rooftop #vibes #golden",
        "twitter": "Sunset mood 🌅💜",
        "telegram": "🌅 Pensamentos do pôr do sol... 💜",
    },
    "life_night_neon": {
        "instagram": "Night city vibes 🌃⚡\nBlade Runner feelings 💜\n{tags}",
        "tiktok": "Night city walking 🌃⚡ #nightcity #neon #cyberpunk #vibes",
        "twitter": "Night city 🌃⚡💜",
        "telegram": "🌃 Night city mode... vibes cyberpunk 💜",
    },
    "life_reading_rainy": {
        "instagram": "Rainy day + livro = perfeição 🌧📚\nO que vocês leem quando chove? 💜\n{tags}",
        "tiktok": "Rainy day reading 🌧📚 #rainy #reading #cozy #asmr",
        "twitter": "Dia de chuva e livro 🌧📚💜",
        "telegram": "🌧 Dia de chuva e livro... perfeito 💜",
    },
}


def catalog_content() -> dict:
    """Catalog all available content."""
    catalog = {
        "generated_at": datetime.now().isoformat(),
        "videos": [],
        "images": [],
        "summary": {},
    }

    # Catalog videos
    if VIDEOS_DIR.exists():
        for f in sorted(VIDEOS_DIR.glob("*.mp4")):
            name = f.stem
            category = "teaser" if "teaser" in name or "reel" in name else \
                       "vip" if "vip" in name else \
                       "lifestyle" if "life" in name else "promo"
            
            captions = CAPTIONS.get(name, {})
            catalog["videos"].append({
                "name": name,
                "file": str(f),
                "size_mb": round(f.stat().st_size / 1024 / 1024, 1),
                "category": category,
                "captions": {
                    platform: caption.replace("{tags}", HASHTAGS.get(platform, ""))
                    for platform, caption in captions.items()
                } if captions else {},
            })

    # Catalog images
    for img_dir in [IMAGES_DIR, LANDING_IMAGES]:
        if img_dir.exists():
            for f in sorted(img_dir.glob("*.png")):
                catalog["images"].append({
                    "name": f.stem,
                    "file": str(f),
                    "size_mb": round(f.stat().st_size / 1024 / 1024, 1),
                    "source": str(img_dir.parent.name),
                })

    # Summary
    catalog["summary"] = {
        "total_videos": len(catalog["videos"]),
        "total_images": len(catalog["images"]),
        "videos_by_category": {},
        "platforms_ready": ["instagram", "tiktok", "twitter", "telegram"],
    }

    for v in catalog["videos"]:
        cat = v["category"]
        catalog["summary"]["videos_by_category"][cat] = \
            catalog["summary"]["videos_by_category"].get(cat, 0) + 1

    return catalog


def print_catalog(catalog: dict):
    """Pretty-print the content catalog."""
    print("=" * 60)
    print("📋 Nairu Content Catalog")
    print("=" * 60)

    print(f"\n🎥 Videos ({catalog['summary']['total_videos']}):")
    for cat, count in catalog["summary"]["videos_by_category"].items():
        print(f"   {cat}: {count}")

    print(f"\n📸 Images ({catalog['summary']['total_images']})")

    print(f"\n🎬 Video Details:")
    for v in catalog["videos"]:
        has_captions = "✅" if v["captions"] else "⚠️ no captions"
        print(f"   [{v['category']:10s}] {v['name']:30s} {v['size_mb']:5.1f}MB  {has_captions}")

    print(f"\n📱 Platforms: {', '.join(catalog['summary']['platforms_ready'])}")
    print("=" * 60)


def export_for_platform(catalog: dict, platform: str):
    """Export content list optimized for a specific platform."""
    export = []
    for v in catalog["videos"]:
        if platform in v.get("captions", {}):
            export.append({
                "file": v["file"],
                "caption": v["captions"][platform],
                "category": v["category"],
            })

    export_path = Path(__file__).parent / f"export_{platform}.json"
    with open(export_path, "w", encoding="utf-8") as f:
        json.dump(export, f, indent=2, ensure_ascii=False)
    print(f"   📁 Exported {len(export)} items → {export_path.name}")
    return export_path


def main():
    print("\n🗂️  Nairu Content Manager\n")

    # Catalog everything
    catalog = catalog_content()
    print_catalog(catalog)

    # Save full catalog
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Full catalog → {OUTPUT_FILE}")

    # Export per platform
    print(f"\n📤 Exporting per platform:")
    for platform in ["instagram", "tiktok", "twitter", "telegram"]:
        export_for_platform(catalog, platform)

    print(f"\n✅ Done! Use exports to schedule posts per platform.")


if __name__ == "__main__":
    main()
