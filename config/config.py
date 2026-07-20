import os

from dotenv import load_dotenv

load_dotenv()

# Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")

# WG-Easy API
WG_API_URL = os.getenv("WG_API_URL")
WG_PASSWORD = os.getenv("WG_PASSWORD")

# WireGuard
WG_HOST = os.getenv("WG_HOST")
WG_PORT = int(os.getenv("WG_PORT", "51820"))

WG_DNS = os.getenv("WG_DNS", "1.1.1.1")
WG_ALLOWED_IPS = os.getenv("WG_ALLOWED_IPS", "0.0.0.0/0, ::/0")

WG_MTU = int(os.getenv("WG_MTU", "1420"))
WG_PERSISTENT_KEEPALIVE = int(
    os.getenv("WG_PERSISTENT_KEEPALIVE", "25")
)