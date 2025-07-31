from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.section_menus import back_to_section_kb
from storage.json_helpers import read_json
from config import DATA_FILES
import os

router = Router()


@router.callback_query(F.data.endswith("_show"))
async def show_all_handler(call: CallbackQuery):
    section = call.data.replace("_show", "")  # получим: schedule, deadlines, exams
    file_path = DATA_FILES.get(section)

    # Check file existence
    if not file_path or not os.path.exists(file_path):
        await call.message.answer("📭 Пока ничего нет.")
        return

    items = read_json(file_path)

    if not items:
        await call.message.answer("📭 Пока ничего нет.")
        return

    # Generate output text
    text = f"📋 <b>{section.capitalize()}:</b>\n\n"

    for i, item in enumerate(items, 1):
        match section:
            case "schedule":
                text += f"{i}. <b>{item['subject']}</b>: {item['time']} ({item['room']}) — {item['day']}\n\n"
            case "deadlines":
                text += (
                    f"{i}. <b>{item['subject']}</b>: {item['task']}\n"
                    f"🔗 <a href='{item['link']}'>файл</a>\n"
                    f"🕒 до {item['deadline']}\n\n"
                )
            case "exams":
                text += f"{i}. <b>{item['subject']}</b>: {item['type']} — {item['datetime']} ({item['room']})\n\n"

    await call.message.answer(
        text,
        parse_mode="HTML",
        reply_markup=back_to_section_kb(section)
    )

