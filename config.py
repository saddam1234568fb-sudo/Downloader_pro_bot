import os
from dotenv import load_dotenv

load_dotenv()

# এখানে ব্র্যাকেটের ভেতরে শুধু "BOT_TOKEN" লেখা থাকবে, আসল টোকেন নয়
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Ensure super admin is always present, plus any added via env
ADMIN_IDS = {6836865426}
env_admins = os.getenv("ADMIN_IDS", "")
if env_admins:
    ADMIN_IDS.update([int(x.strip()) for x in env_admins.split(",") if x.strip().isdigit()])

SUPPORT_CHANNEL = os.getenv("SUPPORT_CHANNEL", "@YourSupportChannel")
BOT_USERNAME = os.getenv("BOT_USERNAME", "Downloader_pro20_bot")
PORT = int(os.getenv("PORT", "10000"))

# Limits & Settings Defaults
MAX_CONCURRENT_DOWNLOADS = int(os.getenv("MAX_CONCURRENT_DOWNLOADS", "2"))
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE", "50"))
MAX_PLAYLIST_ITEMS = int(os.getenv("MAX_PLAYLIST_ITEMS", "10"))

TEMP_DIR = "temp"
DB_PATH = "bot_database.db"

os.makedirs(TEMP_DIR, exist_ok=True)
