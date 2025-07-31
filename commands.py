from aiogram import Bot
from aiogram.types import BotCommand


# Registering bot commands
async def setup_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="call", description="Призвать всех"),    # Call everyone
        BotCommand(command="deadlines", description="Дедлайны"),
        BotCommand(command="schedule", description="Расписание"),
        BotCommand(command="exams", description="Экзамены"),
    ]
    await bot.set_my_commands(commands, scope=None)