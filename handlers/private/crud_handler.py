from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.section_menus import get_section_menu
from storage.selected_section import selected_section

router = Router()


# Handle section button: /schedule, /deadlines, etc.
@router.callback_query(F.data.startswith("menu_"))
async def section_menu_handler(call: CallbackQuery):
    section = call.data.replace("menu_", "")  # Extract section name
    selected_section[call.from_user.id] = section  # Save user’s selected section
    await call.message.edit_text(
        f"📂 Раздел: <b>{section.capitalize()}</b>\nВыбери действие:",
        reply_markup=get_section_menu(section)
    )
    await call.answer()


# Handle "Back" button to section menu
@router.callback_query(F.data.startswith("back_to_"))
async def handle_back_to_section(call: CallbackQuery):
    section = call.data.replace("back_to_", "")
    await call.message.edit_text(
        f"📂 Раздел: <b>{section.capitalize()}</b>\nВыбери действие:",
        reply_markup=get_section_menu(section)
    )
    await call.answer()