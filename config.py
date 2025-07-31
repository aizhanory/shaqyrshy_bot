import os
from dotenv import load_dotenv

load_dotenv()   # Loads variables from .env

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID") or 0)
ALLOWED_CHAT_ID = int(os.getenv("ALLOWED_CHAT_ID") or 0)

# Here file paths
DATA_FILES = {
    "schedule": "storage/schedule.json",
    "deadlines": "storage/deadlines.json",
    "exams": "storage/exams.json"
}

# Ensure BOT_TOKEN is set
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set")
