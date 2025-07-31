from aiogram import Bot
from config import ALLOWED_CHAT_ID


# Schedule (new)
async def send_schedule_added_notification(bot: Bot, entry: dict):
    text = (
        f"🆕📆 Добавлена дисциплина: <b>{entry['subject']}</b>, "
        f"{entry['day']} в {entry['time']} ({entry['room']})"
    )

    await bot.send_message(ALLOWED_CHAT_ID, text, parse_mode="HTML")


# Deadline (new)
async def send_deadline_added_notification(bot: Bot, entry: dict):
    text = (
         f"🆕📁 Добавлен дедлайн: <b>{entry['subject']}</b> – "
         f"{entry['task']} до {entry['deadline']}"
    )
    await bot.send_message(ALLOWED_CHAT_ID, text, parse_mode="HTML", disable_web_page_preview=True)


# Exam (new)
async def send_exam_added_notification(bot: Bot, entry: dict):
    text = (
        f"🆕🎓 Назначен экзамен: <b>{entry['subject']}</b> – "
        f"{entry['type']} {entry['datetime']} ({entry['room']})"
    )
    await bot.send_message(ALLOWED_CHAT_ID, text, parse_mode="HTML")


# Updating
def format_change(field, old, new):
    if old != new:
        return f"{old} ➝ <i>{new}</i>"
    return old


# Schedule (upd.)
async def send_schedule_updated_notification(bot: Bot, old_entry: dict, new_entry: dict):
    text = (
        "<b>❕Изменено расписание:</b>\n\n"
        f"📚 Предмет: {format_change('subject', old_entry['subject'], new_entry['subject'])}\n"
        f"📆 День: {format_change('day', old_entry['day'], new_entry['day'])}\n"
        f"🕒 Время: {format_change('time', old_entry['time'], new_entry['time'])}\n"
        f"🔢 Кабинет: {format_change('room', old_entry['room'], new_entry['room'])}"
    )
    await bot.send_message(ALLOWED_CHAT_ID, text, parse_mode="HTML")


# Deadline (upd.)
async def send_deadline_updated_notification(bot: Bot, old_entry: dict, new_entry: dict):
    text = (
        "<b>❕Изменён дедлайн:</b>\n\n"
        f"📚 Предмет: {format_change('subject', old_entry['subject'], new_entry['subject'])}\n"
        f"📝 Задание: {format_change('task', old_entry['task'], new_entry['task'])}\n"
        f"🕒 Дедлайн: {format_change('deadline', old_entry['deadline'], new_entry['deadline'])}"
    )
    await bot.send_message(ALLOWED_CHAT_ID, text, parse_mode="HTML", disable_web_page_preview=True)


# Exam (upd.)
async def send_exam_updated_notification(bot: Bot, old_entry: dict, new_entry: dict):
    text = (
        "<b>❕Изменён экзамен:</b>\n\n"
        f"📚 Предмет: {format_change('subject', old_entry['subject'], new_entry['subject'])}\n"
        f"📘/ 📕 Тип: {format_change('type', old_entry['type'], new_entry['type'])}\n"
        f"📅 Дата: {format_change('datetime', old_entry['datetime'], new_entry['datetime'])}\n"
        f"🔢 Кабинет: {format_change('room', old_entry['room'], new_entry['room'])}"
    )
    await bot.send_message(ALLOWED_CHAT_ID, text, parse_mode="HTML")