from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from storage.user_state import UserState
from keyboards.confirm_cancel import confirm_cancel_kb
from keyboards.section_menus import back_to_section_kb
from storage.json_helpers import read_json, write_json
from handlers.group.notify import send_deadline_added_notification

router = Router()
DEADLINES_PATH = "storage/deadlines.json"


# Start
@router.callback_query(F.data == "deadlines_add")
async def start_deadline_add(call: CallbackQuery, state: FSMContext):
    await call.message.answer("📚 Напиши предмет:")
    await state.set_state(UserState.deadline_subject)
    await call.answer()


# Subject → Task
@router.message(UserState.deadline_subject)
async def get_deadline_subject(msg: Message, state: FSMContext):
    await state.update_data(subject=msg.text)
    await msg.answer("✍️ Напиши задание:")
    await state.set_state(UserState.deadline_task)


# Task → Link
@router.message(UserState.deadline_task)
async def get_deadline_task(msg: Message, state: FSMContext):
    await state.update_data(task=msg.text)
    await msg.answer("🔗 Вставь ссылку на файл (если нет — напиши `-`):")
    await state.set_state(UserState.deadline_link)


# Link → Date
@router.message(UserState.deadline_link)
async def get_deadline_link(msg: Message, state: FSMContext):
    await state.update_data(link=msg.text)
    await msg.answer("⏰ Укажи дедлайн в формате `ГГГГ-ММ-ДД ЧЧ:ММ`, например: `2025-09-19 16:00`")
    await state.set_state(UserState.deadline_due)


# Parse date and show preview
@router.message(UserState.deadline_due)
async def get_deadline_due(msg: Message, state: FSMContext):
    try:
        datetime.strptime(msg.text, "%Y-%m-%d %H:%M")
        await state.update_data(deadline=msg.text)

        data = await state.get_data()
        preview = (
            f"📌 <b>{data['subject']}</b>\n"
            f"📝 {data['task']}\n"
            f"🔗 {data['link']}\n"
            f"🕒 до <u>{data['deadline']}</u>"
        )
        await msg.answer(f"Проверь:\n\n{preview}", parse_mode="HTML", reply_markup=confirm_cancel_kb("deadlines"))
    except ValueError:
        await msg.answer("⚠️ Формат некорректен. Пример: `2025-09-19 16:00`", parse_mode="Markdown")


# Save to JSON
@router.callback_query(F.data == "confirm_deadlines")
async def save_deadline(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    new_entry = {
        "subject": data["subject"],
        "task": data["task"],
        "link": data["link"],
        "deadline": data["deadline"]
    }

    all_data = read_json(DEADLINES_PATH)
    all_data.append(new_entry)
    write_json(DEADLINES_PATH, all_data)

    await call.message.edit_text("✅ Дедлайн добавлен!", reply_markup=back_to_section_kb("deadlines"))
    await send_deadline_added_notification(call.bot, new_entry)
    await state.clear()
    await call.answer()


# Cancel
@router.callback_query(F.data == "confirm_cancel_deadlines")
async def cancel_deadline(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("❌ Отменено.", reply_markup=back_to_section_kb("deadlines"))
    await state.clear()
    await call.answer()