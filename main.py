import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN
from commands import setup_bot_commands
from hybrid_middleware import HybridMiddleware

# Handlers
from handlers.private import start, crud_handler, show_all, delete_flow, edit_flow
from handlers.private.flows import add_schedule, add_exam, add_deadline
from handlers.group.notify_deadline_end import setup_scheduler
from handlers.group import call


async def main():
    # Initialize bot and dispatcher
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=MemoryStorage())

    # Middleware for both private and group messages
    hybrid = HybridMiddleware()
    dp.message.middleware(hybrid)
    dp.chat_member.middleware(hybrid)

    # Registering all routers
    dp.include_routers(
        start.router,
        crud_handler.router,
        show_all.router,
        delete_flow.router,
        edit_flow.router,
        add_schedule.router,
        add_deadline.router,
        add_exam.router,
        call.router
    )

    setup_scheduler(bot)

    print("🤖 Бот запущен.")  # Bot started
    await setup_bot_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Entry point
    asyncio.run(main())