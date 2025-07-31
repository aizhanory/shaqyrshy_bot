from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from storage.user_state import UserState
from keyboards.confirm_cancel import confirm_cancel_kb
from keyboards.section_menus import back_to_section_kb
from storage.json_helpers import read_json, write_json
from handlers.group.notify import send_exam_added_notification

router = Router()
EXAMS_PATH = "storage/exams.json"


# Start
@router.callback_query(F.data == "exams_add")
async def start_exam_add(call: CallbackQuery, state: FSMContext):
    await call.message.answer("📘 Напиши предмет:")
    await state.set_state(UserState.exam_subject)
    await call.answer()


# Subject → Type
@router.message(UserState.exam_subject)
async def get_exam_subject(msg: Message, state: FSMContext):
    await state.update_data(subject=msg.text)
    await msg.answer("🎯 Укажи тип (Рубежка / Сессия):")
    await state.set_state(UserState.exam_type)


# Validate type → Ask datetime
@router.message(UserState.exam_type)
async def get_exam_type(msg: Message, state: FSMContext):
    exam_type = msg.text.strip().lower()
    if exam_type not in ["рубежка", "сессия"]:
        await msg.answer("⚠️ Напиши 'Рубежка' или 'Сессия'")
        return
    await state.update_data(type=msg.text)
    await msg.answer("📅 Укажи дату и время (напр. `2025-09-19 17:00 - 18:00`):")
    await state.set_state(UserState.exam_datetime)


# Parse datetime → Ask room
@router.message(UserState.exam_datetime)
async def get_exam_datetime(msg: Message, state: FSMContext):
    try:
        datetime.strptime(msg.text.split(" - ")[0], "%Y-%m-%d %H:%M")
    except ValueError:
        await msg.answer("⚠️ Формат неверный. Пример: `2025-09-19 17:00 - 18:00`")
        return
    await state.update_data(datetime=msg.text)
    await msg.answer("🏫 Укажи кабинет / блок:")
    await state.set_state(UserState.exam_room)


# Room → Show preview
@router.message(UserState.exam_room)
async def get_exam_room(msg: Message, state: FSMContext):
    await state.update_data(room=msg.text)
    data = await state.get_data()
    preview = (
        f"📘 <b>{data['subject']}</b> — {data['type']}\n"
        f"🕒 {data['datetime']}\n"
        f"🔢 {data['room']}"
    )
    await msg.answer(f"Проверь:\n\n{preview}", parse_mode="HTML", reply_markup=confirm_cancel_kb("exams"))


# Save to JSON file
@router.callback_query(F.data == "confirm_exams")
async def save_exam(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    new_entry = {
        "subject": data["subject"],
        "type": data["type"],
        "datetime": data["datetime"],
        "room": data["room"]
    }

    all_data = read_json(EXAMS_PATH)
    all_data.append(new_entry)
    write_json(EXAMS_PATH, all_data)

    await call.message.edit_text("✅ Экзамен добавлен!", reply_markup=back_to_section_kb("exams"))
    await send_exam_added_notification(call.bot, new_entry)
    await state.clear()
    await call.answer()


# Cancel
@router.callback_query(F.data == "confirm_cancel_exams")
async def cancel_exam(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("❌ Отменено.", reply_markup=back_to_section_kb("exams"))
    await state.clear()
    await call.answer()



