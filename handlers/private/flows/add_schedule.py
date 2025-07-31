from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from storage.user_state import UserState
from keyboards.confirm_cancel import confirm_cancel_kb
from keyboards.section_menus import back_to_section_kb
from storage.json_helpers import read_json, write_json
from handlers.group.notify import send_schedule_added_notification

router = Router()

SCHEDULE_FILE = "storage/schedule.json"


# Start
@router.callback_query(F.data == "schedule_add")
async def start_add_schedule(call:CallbackQuery, state: FSMContext):
    await state.set_state(UserState.schedule_subject)
    await call.message.answer("Напиши название предмета (напр. Математика):")
    await call.answer()


# Subject → Day
@router.message(UserState.schedule_subject)
async def set_subject(message: Message, state: FSMContext):
    await state.update_data(subject=message.text.strip())
    await state.set_state(UserState.schedule_day)
    await message.answer("📆 Напиши день недели (напр. Вторник):")


# Day → Time
@router.message(UserState.schedule_day)
async def set_day(message: Message, state: FSMContext):
    await state.update_data(day=message.text.strip())
    await state.set_state(UserState.schedule_time)
    await message.answer("🕒 Напиши время (напр. 18:00 - 19:00):")


# Time → Room
@router.message(UserState.schedule_time)
async def set_time(message: Message, state: FSMContext):
    await state.update_data(time=message.text.strip())
    await state.set_state(UserState.schedule_room)
    await message.answer("🔢 Напиши кабинет/блок (напр. 502/3):")


# Room → Show preview
@router.message(UserState.schedule_room)
async def set_room(message: Message, state: FSMContext):
    await state.update_data(room=message.text.strip())
    data = await state.get_data()

    text = (
        f"📚 *Предмет:* {data['subject']}\n"
        f"📆 *День:* {data['day']}\n"
        f"🕒 *Время:* {data['time']}\n"
        f"🔢 *Кабинет:* {data['room']}"
    )

    await message.answer(
        f"Проверь данные перед сохранением:\n\n{text}",
        parse_mode="Markdown",
        reply_markup=confirm_cancel_kb("schedule")
    )


# Save to JSON file
@router.callback_query(F.data == "confirm_schedule")
async def confirm_yes(call: CallbackQuery, state: FSMContext):
    global schedule
    data = await state.get_data()
    new_entry = {
        "subject": data["subject"],
        "day": data["day"],
        "time": data["time"],
        "room": data["room"]
    }

    all_data = read_json(SCHEDULE_FILE)
    all_data.append(new_entry)
    write_json(SCHEDULE_FILE, all_data)

    await call.message.edit_text("✅ Сохранено!", reply_markup=back_to_section_kb("schedule"))
    await send_schedule_added_notification(call.bot, new_entry)

    await state.clear()
    await call.answer()


# Cancel
@router.callback_query(F.data == "confirm_cancel_schedule")
async def cancel_add(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("❌ Отменено.", reply_markup=back_to_section_kb("schedule"))
    await state.clear()
    await call.answer()

