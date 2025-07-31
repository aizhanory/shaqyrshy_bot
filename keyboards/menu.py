from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📅 Расписание", callback_data="menu_schedule")],
    [InlineKeyboardButton(text="📌 Дедлайны", callback_data="menu_deadlines")],
    [InlineKeyboardButton(text="📚 Экзамены", callback_data="menu_exams")]
])

