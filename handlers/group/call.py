from aiogram import Router, F
from aiogram.types import Message, ChatMemberUpdated
from aiogram.enums.chat_member_status import ChatMemberStatus
from storage.json_helpers import read_json, write_json
from aiogram.enums.chat_type import ChatType
from config import DATA_FILES
from datetime import datetime
import pytz

router = Router()
router.message.filter(F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}))


# Bot greets after being added to a group
@router.my_chat_member()
async def bot_added(event: ChatMemberUpdated):
    old_status = event.old_chat_member.status
    new_status = event.new_chat_member.status

    if old_status in {ChatMemberStatus.LEFT, ChatMemberStatus.KICKED} and \
            new_status in {ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR}:

        # Print to terminal
        print("🤖 Bot added to a group.")
        print(f"🆔 Group Chat ID: {event.chat.id}")
        print(f"👤 Admin/User ID: {event.from_user.id}")

        await event.bot.send_message(
            chat_id=event.chat.id,
            text=(
                "👋🏼 Привет! Я – <b>Shaqyrshy Bot</b>.\n\n"
                "📣 <b>/call</b> – Призвать всех\n"
                "📅 <b>/schedule</b> – Расписание\n"
                "📁 <b>/deadlines</b> – Дедлайны\n"
                "🎓 <b>/exams</b> – Рубежки\Сессии \n"
                "🗣 Также отзовусь на слова «шакырш», «шақыршы»\n\n"
                "<i>Если что-то изменится – постараюсь вовремя сообщать.</i>"
            ),
            parse_mode="HTML"
        )


# /call — mentions each member in group
@router.message(F.text.startswith("/call"))
async def call_everyone(message: Message):
    members = await message.chat.get_administrators()
    bot_user = await message.bot.get_me()

    mentions = []
    for member in members:
        user = member.user
        if user.id == bot_user.id:
            continue  # Skip the bot itself

        if user.username:
            mentions.append(f"@{user.username}")
        else:
            name = user.first_name or "Пользователь"
            mentions.append(f"<a href='tg://user?id={user.id}'>{name}</a>")

    if not mentions:
        await message.answer("❌ Никого не нашёл для призыва.")
        return

    await message.answer("📣 Призыв: " + " ".join(mentions), parse_mode="HTML")


# Responds to trigger words like "shaqyrshy"
@router.message(
    F.text,
    F.text.func(lambda text: not text.startswith("/") and any(word in text.lower() for word in {
        "шакырш", "шақыршы", "шақырш", "shaqyrshy",
        "шақыр", "shaqyrsh"
    }))
)
async def call_keyword_trigger(message: Message):
    members = await message.chat.get_administrators()
    bot_user = await message.bot.get_me()
    mentions = []

    for member in members:
        user = member.user
        if user.id == bot_user.id:
            continue  # Skip the bot

        if user.username:
            mentions.append(f"@{user.username}")
        else:
            name = user.first_name or "пользователь"
            mentions.append(f"<a href='tg://user?id={user.id}'>{name}</a>")

    await message.answer("Біреу шақырып жатыр 👀 \n" + " ".join(mentions), parse_mode="HTML")


# /schedule — shows whole schedule
@router.message(F.text.regexp(r"^/schedule(@\w+)?$"))
async def show_schedule(message: Message):
    data = read_json(DATA_FILES["schedule"])
    if not data:
        await message.answer("📅 Расписание пока не добавлено.")
        return

    weekday_order = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]
    grouped = {day: [] for day in weekday_order}

    # groups by week days
    for item in data:
        day = item["day"].strip().capitalize()
        if day in grouped:
            grouped[day].append(item)
        else:
            grouped.setdefault("Прочее", []).append(item)

    # sorts by start time
    for day in grouped:
        grouped[day].sort(
            key=lambda x: datetime.strptime(
                x["time"].replace("—", "-").split("-")[0].strip(),
                "%H:%M"
            )
        )

    # builds respond
    text = "📅 <b>Расписание:</b>\n\n"
    for day in weekday_order:
        items = grouped.get(day, [])
        if items:
            text += f"<b>{day}</b>\n\n"
            for item in items:
                text += f"  • <b>{item['subject']}</b>: {item['time']} ({item['room']})\n"
            text += "\n"

    if "Прочее" in grouped:
        text += "<b>Другие дни</b>\n"
        for item in grouped["Прочее"]:
            text += f"<b>{item['subject']}</b>: {item['day']} {item['time']} ({item['room']})\n"

    await message.answer(text.strip(), parse_mode="HTML")


# /deadlines - shows deadlines
@router.message(F.text.regexp(r"^/deadlines(@\w+)?$"))
async def show_deadlines(message: Message):
    data = read_json(DATA_FILES["deadlines"])
    if not data:
        await message.answer("📁 Пока дедлайнов нет или они уже истекли.")
        return

    timezone = pytz.timezone("Asia/Almaty")
    now = datetime.now(timezone)

    updated = []

    for item in data:
        try:
            dt = timezone.localize(datetime.strptime(item["deadline"], "%Y-%m-%d %H:%M"))
            if dt > now:
                left = dt - now
                days, hours = left.days, left.seconds // 3600
                mins = (left.seconds % 3600) // 60
                item["__time_left"] = f"{days}д {hours}ч {mins}м"
                item["__parsed"] = dt
                updated.append(item)
        except ValueError:
            continue

    if not updated:
        await message.answer("📁 Пока дедлайнов нет или они уже истекли.")
        return

    updated.sort(key=lambda x: x["__parsed"])

    text = "📁 <b>Дедлайны:</b>\n\n"
    for i in updated:
        link = f" (<a href='{i['link']}'>файл</a>)" if i.get("link") and i["link"] != "-" else ""
        text += (
            f"  • <b>{i['subject']}</b>: {i['task']}{link} – до {i['deadline']} "
            f"(<i>{i['__time_left']}</i>)\n"
        )

    await message.answer(text.strip(), parse_mode="HTML", disable_web_page_preview=True)


# /exams — shows upcoming exams (midterms/finals), auto-removes expired ones
@router.message(F.text.regexp(r"^/exams(@\w+)?$"))
async def show_exams(message: Message):
    data = read_json(DATA_FILES["exams"])
    if not data:
        await message.answer("🎓 Экзамены пока не добавлены.")
        return

    timezone = pytz.timezone("Asia/Almaty")
    now = datetime.now(timezone)

    exams_midterm = []
    exams_final = []
    expired = []

    for item in data:
        try:
            # parse "2025-09-19 17:00 - 18:00" → takes the start datetime
            date_part = item["datetime"].split(" ")[0]
            time_part = item["datetime"].split(" ")[1]
            parsed_dt = timezone.localize(datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H:%M"))
            item["__parsed"] = parsed_dt

            if parsed_dt < now:
                expired.append(item)
                continue

            exam_type = item["type"].strip().lower()
            if "рубеж" in exam_type or "рубек" in exam_type:
                exams_midterm.append(item)
            elif "сесс" in exam_type:
                exams_final.append(item)
        except ValueError:
            continue

    # no upcoming exams left
    if not exams_midterm and not exams_final:
        await message.answer("🎓 Пока экзаменов нет или они уже прошли.")
        return

    # sorts by date
    exams_midterm.sort(key=lambda x: x["__parsed"])
    exams_final.sort(key=lambda x: x["__parsed"])

    text = "🎓 <b>Экзамены:</b>\n\n"

    if exams_midterm:
        text += "<b>📘 Рубежки:</b>\n"
        for i in exams_midterm:
            text += f" <b>{i['subject']}</b> – {i['datetime']} ({i['room']})\n"
        text += "\n"

    if exams_final:
        text += "<b>📕 Сессии:</b>\n"
        for i in exams_final:
            text += f" <b>{i['subject']}</b> – {i['datetime']} ({i['room']})\n"

    await message.answer(text.strip(), parse_mode="HTML")
