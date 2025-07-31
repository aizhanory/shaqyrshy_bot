from aiogram import Router, F
from aiogram.types import (
    CallbackQuery, Message, InlineKeyboardButton,
    InlineKeyboardMarkup)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from storage.selected_section import selected_section
from storage.json_helpers import read_json, write_json
from handlers.group.notify import (
    send_schedule_updated_notification,
    send_deadline_updated_notification,
    send_exam_updated_notification
)
from urllib.parse import urlparse
from config import DATA_FILES
from typing import List, Dict

router = Router()


class EditState(StatesGroup):
    waiting_for_item = State()
    waiting_for_field = State()
    waiting_for_value = State()
    confirm = State()


# Step 1: Edit pressed
@router.callback_query(F.data.endswith("_edit"))
async def start_edit(call: CallbackQuery, state: FSMContext):
    section = call.data.removesuffix("_edit")
    selected_section[call.from_user.id] = section
    path = DATA_FILES.get(section)

    if not path:
        await call.message.answer("❌ Файл не найден.")
        return

    data = read_json(path)
    if not data:
        await call.message.answer("📭 Пока ничего нет.")
        return

    buttons = []
    for i, item in enumerate(data):
        if section == "schedule":
            btn_text = f"{item['day']}: {item['subject']} ({item['time']}) - {item['room']}"
        elif section == "deadlines":
            if item["link"] and item["link"] != "-":
                domain = urlparse(item["link"]).netloc
                link_preview = f" [📎 {domain}]"
            else:
                link_preview = ""
            btn_text = f"{item['subject']}: {item['task']} до {item['deadline']}{link_preview}"
        elif section == "exams":
            btn_text = f"{item['subject']} — {item['type']} ({item['datetime']}) - {item['room']}"
        else:
            continue

        buttons.append([InlineKeyboardButton(text=btn_text, callback_data=f"edit_{i}")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await call.message.edit_text("✏️ Что вы хотите изменить?", reply_markup=keyboard)
    await state.set_state(EditState.waiting_for_item)


# Step 2: Item selected
@router.callback_query(F.data.startswith("edit_"))
async def select_item(call: CallbackQuery, state: FSMContext):
    index = int(call.data.split("_")[1])
    section = selected_section.get(call.from_user.id)

    await state.update_data(index=index, section=section)

    if section == "schedule":
        fields = ["subject", "day", "time", "room"]
    elif section == "deadlines":
        fields = ["subject", "task", "link", "deadline"]
    elif section == "exams":
        fields = ["subject", "type", "datetime", "room"]
    else:
        await call.answer("❌ Неизвестный раздел.")
        return

    field_names = {
        "subject": "Предмет",
        "day": "День недели",
        "time": "Время",
        "room": "Аудитория",
        "task": "Задание",
        "link": "Ссылка",
        "deadline": "Дедлайн",
        "type": "Тип экзамена",
        "datetime": "Дата и время"
    }

    buttons = [[InlineKeyboardButton(text=field_names[f], callback_data=f"field_{f}")] for f in fields]
    await call.message.edit_text("Что именно вы хотите изменить?", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    await state.set_state(EditState.waiting_for_field)


# Step 3: Field selected
@router.callback_query(F.data.startswith("field_"))
async def choose_field(call: CallbackQuery, state: FSMContext):
    field = call.data.replace("field_", "")
    await state.update_data(field=field)

    field_names = {
        "subject": "предмет",
        "day": "день недели",
        "time": "время",
        "room": "аудиторию",
        "task": "задание",
        "link": "ссылку",
        "deadline": "дедлайн",
        "type": "тип экзамена",
        "datetime": "дату и время"
    }
    pretty = field_names.get(field, field)

    await call.message.answer(f"✍️ Введите новое значение для {pretty}:")
    await state.set_state(EditState.waiting_for_value)


# Step 4: Value input
@router.message(EditState.waiting_for_value)
async def receive_value(msg: Message, state: FSMContext):
    user_data = await state.get_data()
    section = user_data["section"]
    index = user_data["index"]
    field = user_data["field"]
    path = DATA_FILES[section]

    data: List[Dict[str, str]] = read_json(path)
    old_entry = data[index].copy()
    data[index][field] = msg.text
    new_entry = data[index]

    write_json(path, data)

    await msg.answer("✅ Изменено! Возвращаюсь в меню.")
    await state.clear()

    match section:
        case "schedule":
            await send_schedule_updated_notification(msg.bot, old_entry, new_entry)
        case "deadlines":
            await send_deadline_updated_notification(msg.bot, old_entry, new_entry)
        case "exams":
            await send_exam_updated_notification(msg.bot, old_entry, new_entry)
