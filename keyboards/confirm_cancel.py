from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def confirm_cancel_kb(section: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"confirm_{section}")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data=f"confirm_cancel_{section}")]
    ])