from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Universal menu
def get_section_menu(section: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Добавить", callback_data=f"{section}_add")],
        [InlineKeyboardButton(text="Изменить", callback_data=f"{section}_edit")],
        [InlineKeyboardButton(text="Удалить", callback_data=f"{section}_delete")],
        [InlineKeyboardButton(text="Посмотреть все", callback_data=f"{section}_show")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_main")]
    ])


def back_to_section_kb(section: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data=f"back_to_{section}")]
    ])