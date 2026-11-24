
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL")
WEBHOOK_BASE_URL = os.getenv("WEBHOOK_BASE_URL")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

WEBHOOK_PATH = "/telegram/webhook"

if not all([
    BOT_TOKEN,
    WEBAPP_URL,
    WEBHOOK_BASE_URL,
    WEBHOOK_SECRET
]):
    raise ValueError("ENV konfiguratsiyasi to'liq emas")

WEBHOOK_URL = (
    WEBHOOK_BASE_URL.rstrip("/")
    + WEBHOOK_PATH
)
