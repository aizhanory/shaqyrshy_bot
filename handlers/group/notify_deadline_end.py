from datetime import datetime
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from storage.json_helpers import read_json, write_json
from config import DATA_FILES, ALLOWED_CHAT_ID
import pytz

tz = pytz.timezone("Asia/Almaty")


async def check_deadlines(bot: Bot):
    data = read_json(DATA_FILES["deadlines"])
    now = datetime.now(tz)
    updated = []

    for item in data:
        try:
            deadline = tz.localize(datetime.strptime(item["deadline"], "%Y-%m-%d %H:%M"))
            if now >= deadline:
                await bot.send_message(
                    ALLOWED_CHAT_ID,
                    f"❗ Дедлайн по <b>{item['subject']}</b> истёк\n",
                    parse_mode="HTML"
                )
            else:
                updated.append(item)
        except ValueError:
            updated.append(item)

    write_json(DATA_FILES["deadlines"], updated)


def setup_scheduler(bot: Bot):
    scheduler = AsyncIOScheduler(timezone=tz)
    scheduler.add_job(check_deadlines, "interval", seconds=10, args=[bot])
    scheduler.start()
