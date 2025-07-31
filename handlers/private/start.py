from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from config import ADMIN_ID
from keyboards.menu import main_menu

router = Router()


# Handle /start command
@router.message(F.text == "/start")
async def start_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ У вас нет доступа к управлению ботом.")
        return

    await message.answer("Привет! 👋 Выбери раздел:", reply_markup=main_menu)


# Handle "Back to main menu" button
@router.callback_query(F.data == "back_to_main")
async def back_to_main_handler(call: CallbackQuery):
    if call.from_user.id != ADMIN_ID:
        await call.answer("⛔ Нет доступа", show_alert=True)
        return

    await call.message.edit_text("📋 Главное меню:", reply_markup=main_menu)
    await call.answer()