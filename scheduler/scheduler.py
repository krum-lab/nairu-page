"""
Nairu Content Scheduler V2 — Auto-post to multiple platforms
Supports: Instagram (instagrapi), Twitter/X (tweepy), Telegram (aiogram)
Loads content from content_manager exports.
Run: python scheduler.py [--now] [--platform instagram|twitter|telegram]
"""

import os
import sys
import json
import time
import schedule
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load env
env_path = Path(__file__).parent.parent / "telegram-bot" / ".env"
load_dotenv(env_path)

# Content library
CONTENT_DIR = Path(__file__).parent.parent / "instagram" / "content"
VIDEOS_DIR = Path(__file__).parent.parent / "video-generator" / "output"
SCHEDULE_FILE = Path(__file__).parent / "schedule_v2.json"
EXPORTS_DIR = Path(__file__).parent.parent / "content-manager"

# ============================================================
# LOAD CONTENT FROM EXPORTS
# ============================================================

def load_platform_content(platform: str) -> list:
    """Load content catalog export for a platform."""
    export_file = EXPORTS_DIR / f"export_{platform}.json"
    if export_file.exists():
        with open(export_file, encoding="utf-8") as f:
            return json.load(f)
    return []


# Full content calendar — all available content with scheduling state
def build_content_calendar() -> list:
    """Build content calendar from all sources."""
    calendar = []

    # Load from all platform exports
    for platform in ["instagram", "twitter", "telegram"]:
        items = load_platform_content(platform)
        for item in items:
            file_path = Path(item["file"])
            if not file_path.exists():
                continue

            # Check if already in calendar
            existing = next(
                (c for c in calendar if c["file"] == item["file"]),
                None
            )
            if existing:
                if platform not in existing["platforms"]:
                    existing["platforms"].append(platform)
                    existing["captions"][platform] = item["caption"]
            else:
                calendar.append({
                    "type": "video" if file_path.suffix == ".mp4" else "image",
                    "file": item["file"],
                    "name": file_path.stem,
                    "category": item.get("category", "general"),
                    "captions": {platform: item["caption"]},
                    "platforms": [platform],
                    "posted": {},
                })

    # Also add image posts from instagram/content
    if CONTENT_DIR.exists():
        for img in sorted(CONTENT_DIR.glob("*.png")):
            existing = next(
                (c for c in calendar if Path(c["file"]).name == img.name),
                None
            )
            if not existing:
                calendar.append({
                    "type": "image",
                    "file": str(img),
                    "name": img.stem,
                    "category": "image_post",
                    "captions": {
                        "instagram": f"✨💜 {img.stem.replace('_', ' ').title()}\n#gamergirl #anime #otaku #cosplay",
                    },
                    "platforms": ["instagram"],
                    "posted": {},
                })

    return calendar


# ============================================================
# POSTING FUNCTIONS
# ============================================================

def post_to_instagram(content: dict) -> bool:
    """Post content to Instagram using instagrapi."""
    try:
        from instagrapi import Client as IGClient
    except ImportError:
        print("  ⚠️ instagrapi not installed. Run: pip install instagrapi")
        return False

    ig_user = os.getenv("INSTAGRAM_USERNAME")
    ig_pass = os.getenv("INSTAGRAM_PASSWORD")
    if not ig_user or not ig_pass:
        print("  ⚠️ INSTAGRAM_USERNAME/PASSWORD not in .env")
        return False

    ig = IGClient()
    ig.login(ig_user, ig_pass)

    file_path = content["file"]
    caption = content["captions"].get("instagram", "💜")

    if content["type"] == "image":
        ig.photo_upload(file_path, caption)
    else:
        ig.clip_upload(file_path, caption)  # Reels for videos

    print(f"  ✅ Instagram: {content['name']}")
    return True


def post_to_twitter(content: dict) -> bool:
    """Post content to Twitter/X using tweepy."""
    try:
        import tweepy
    except ImportError:
        print("  ⚠️ tweepy not installed. Run: pip install tweepy")
        return False

    api_key = os.getenv("TWITTER_API_KEY")
    api_secret = os.getenv("TWITTER_API_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_secret = os.getenv("TWITTER_ACCESS_SECRET")

    if not all([api_key, api_secret, access_token, access_secret]):
        print("  ⚠️ Twitter credentials not in .env")
        return False

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    file_path = content["file"]
    tweet_text = content["captions"].get("twitter", "💜")[:270]
    media = api.media_upload(file_path)
    api.update_status(tweet_text, media_ids=[media.media_id])

    print(f"  ✅ Twitter: {content['name']}")
    return True


async def post_to_telegram(content: dict) -> bool:
    """Post content to Telegram channel/group."""
    from aiogram import Bot

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    channel = os.getenv("TELEGRAM_CHANNEL_ID")

    if not token or not channel:
        print("  ⚠️ TELEGRAM_BOT_TOKEN/CHANNEL_ID not in .env")
        return False

    bot = Bot(token=token)
    caption = content["captions"].get("telegram", "💜")
    file_path = content["file"]

    try:
        if content["type"] == "video":
            from aiogram.types import FSInputFile
            video = FSInputFile(file_path)
            await bot.send_video(channel, video, caption=caption)
        else:
            from aiogram.types import FSInputFile
            photo = FSInputFile(file_path)
            await bot.send_photo(channel, photo, caption=caption)
        print(f"  ✅ Telegram: {content['name']}")
        return True
    except Exception as e:
        print(f"  ❌ Telegram error: {e}")
        return False
    finally:
        await bot.session.close()


# ============================================================
# SCHEDULER LOGIC
# ============================================================

def load_schedule() -> list:
    """Load existing schedule state or build new one."""
    if SCHEDULE_FILE.exists():
        with open(SCHEDULE_FILE, encoding="utf-8") as f:
            return json.load(f)
    return build_content_calendar()


def save_schedule(calendar: list):
    """Save schedule state to disk."""
    with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
        json.dump(calendar, f, indent=2, ensure_ascii=False)


def get_next_unposted(calendar: list, platform: str = None) -> dict | None:
    """Get next unposted content, optionally filtered by platform."""
    for item in calendar:
        if platform:
            if platform in item["platforms"] and platform not in item.get("posted", {}):
                return item
        else:
            # Find any item not fully posted to all platforms
            for p in item["platforms"]:
                if p not in item.get("posted", {}):
                    return item
    return None


def run_scheduled_post(calendar: list, platform: str = None):
    """Post the next unscheduled content."""
    item = get_next_unposted(calendar, platform)
    if not item:
        print("✅ All content has been posted!")
        return

    print(f"\n📤 Posting: {item['name']} ({item['category']})")

    platforms = [platform] if platform else item["platforms"]
    for p in platforms:
        if p in item.get("posted", {}):
            continue

        success = False
        try:
            if p == "instagram":
                success = post_to_instagram(item)
            elif p == "twitter":
                success = post_to_twitter(item)
            elif p == "telegram":
                import asyncio
                success = asyncio.run(post_to_telegram(item))
        except Exception as e:
            print(f"  ❌ {p}: {e}")

        if success:
            if "posted" not in item:
                item["posted"] = {}
            item["posted"][p] = datetime.now().isoformat()

    save_schedule(calendar)


def main():
    print("=" * 60)
    print("📅 Nairu Content Scheduler V2")
    print("=" * 60)

    calendar = load_schedule()

    # Stats
    total = len(calendar)
    videos = sum(1 for c in calendar if c["type"] == "video")
    images = sum(1 for c in calendar if c["type"] == "image")

    pending_ig = sum(1 for c in calendar if "instagram" in c.get("platforms", [])
                     and "instagram" not in c.get("posted", {}))
    pending_tw = sum(1 for c in calendar if "twitter" in c.get("platforms", [])
                     and "twitter" not in c.get("posted", {}))
    pending_tg = sum(1 for c in calendar if "telegram" in c.get("platforms", [])
                     and "telegram" not in c.get("posted", {}))

    print(f"📦 Total: {total} items ({videos} videos, {images} images)")
    print(f"📱 Pending: IG={pending_ig} | TW={pending_tw} | TG={pending_tg}")
    print(f"⏰ Schedule: Every day at 10:00, 14:00, 19:00")
    print("=" * 60)

    # Parse args
    platform_filter = None
    if "--platform" in sys.argv:
        idx = sys.argv.index("--platform")
        if idx + 1 < len(sys.argv):
            platform_filter = sys.argv[idx + 1]
            print(f"🎯 Filtering: {platform_filter}")

    if "--now" in sys.argv:
        print("\n🚀 Posting now...")
        run_scheduled_post(calendar, platform_filter)
        return

    if "--status" in sys.argv:
        print("\n📊 Content Status:")
        for item in calendar:
            posted = item.get("posted", {})
            status = " | ".join([
                f"{p}: {'✅' if p in posted else '⏳'}"
                for p in item["platforms"]
            ])
            print(f"  {item['name']:30s} [{item['category']:10s}] {status}")
        return

    if "--rebuild" in sys.argv:
        print("\n🔄 Rebuilding calendar from exports...")
        calendar = build_content_calendar()
        save_schedule(calendar)
        print(f"✅ Calendar rebuilt with {len(calendar)} items")
        return

    # Schedule 3 posts per day
    schedule.every().day.at("10:00").do(run_scheduled_post, calendar, platform_filter)
    schedule.every().day.at("14:00").do(run_scheduled_post, calendar, platform_filter)
    schedule.every().day.at("19:00").do(run_scheduled_post, calendar, platform_filter)

    save_schedule(calendar)

    print("\n🔄 Scheduler running... Press Ctrl+C to stop")
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
