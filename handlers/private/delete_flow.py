from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from storage.selected_section import selected_section
from storage.json_helpers import read_json, write_json
from config import DATA_FILES
import os

router = Router()


# Step 1: Show list of items to delete
@router.callback_query(F.data.endswith("_delete"))
async def show_delete_options(call: CallbackQuery):
    section = call.data.replace("_delete", "")
    selected_section[call.from_user.id] = section

    path = DATA_FILES.get(section)
    if not path or not os.path.exists(path):
        await call.message.answer("❌ Файл не найден.")
        return

    data = read_json(path)

    if not data:
        await call.message.answer("📭 Пока ничего нет.")
        return

    text = f"🗑 Что удалить из <b>{section.capitalize()}</b>:\n\n"
    buttons = []

    for i, item in enumerate(data):
        match section:
            case "schedule":    # Format: Day: Subject (Time) - Room
                line = f"{item['subject']} ({item['time']}) - {item['room']}"
                label = f"{item['day']}: {line}"
                text += f"{item['day']}:\n{line}\n"
                buttons.append([InlineKeyboardButton(text=label, callback_data=f"delete_{section}_{i}")])
            case "deadlines":   # Format: Subject: Task
                label = f"{item['subject']}: {item['task']}"
                text += f"{label}\n"
                buttons.append([InlineKeyboardButton(text=label, callback_data=f"delete_{section}_{i}")])
            case "exams":   # Format: Subject — Type (Datetime)
                label = f"{item['subject']} — {item['type']} ({item['datetime']})"
                text += f"{label}\n"
                buttons.append([InlineKeyboardButton(text=label, callback_data=f"delete_{section}_{i}")])
    # Add "Back" button
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data=f"back_to_{section}")])

    await call.message.answer(
        text="👇 Выбери, что удалить:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode="HTML"
    )
    await call.answer()


# Step 2: Handle delete confirmation
@router.callback_query(F.data.startswith("delete_"))
async def handle_delete_by_button(call: CallbackQuery):
    parts = call.data.split("_")
    section = parts[1]
    index = int(parts[2])
    path = DATA_FILES.get(section)

    if not path or not os.path.exists(path):
        await call.message.answer("❌ Файл не найден.")
        return

    data = read_json(path)

    try:
        removed = data.pop(index)
    except IndexError:
        await call.message.answer("❌ Элемент не найден.")
        return

    write_json(path, data)
    # If nothing left — inform and stop
    if not data:
        await call.message.edit_text("✅ Элемент удалён. 📭 Больше ничего не осталось в этом разделе.")
        await call.answer()
        return

    # Show an updated list
    text = f"✅ Удалено. Обновлённый список <b>{section.capitalize()}:</b>\n\n"

    for i, item in enumerate(data, 1):
        match section:
            case "schedule":
                text += f"{i}. {item['subject']} ({item['time']}) - {item['room']}\n"
            case "deadlines":
                text += f"{i}. {item['subject']}: {item['task']} — до {item['deadline']}\n"
            case "exams":
                text += f"{i}. {item['subject']} ({item['type']}) — {item['datetime']} в {item['room']}\n"
        text += "\n"

    back_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Вернуться в меню", callback_data="back_to_main")]
    ])

    await call.message.edit_text(text, reply_markup=back_kb, parse_mode="HTML")
    await call.answer()
