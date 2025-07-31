from aiogram import BaseMiddleware
from aiogram.types import Message, ChatMemberUpdated
from typing import Callable, Awaitable, Dict, Any
from config import ALLOWED_CHAT_ID, ADMIN_ID


class HybridMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        # Group message — allowed only in a specific group
        if hasattr(event, "chat") and event.chat.type in ("group", "supergroup"):
            if event.chat.id == ALLOWED_CHAT_ID:
                return await handler(event, data)
            return None

        # Private message — allowed only for admin
        if hasattr(event, "chat") and event.chat.type == "private":
            if event.from_user.id == ADMIN_ID:
                return await handler(event, data)
            return None

        # ChatMemberUpdated — welcome or system join
        if isinstance(event, ChatMemberUpdated):
            if event.chat.id == ALLOWED_CHAT_ID:
                return await handler(event, data)
            return None
        return None  # Other cases — ignored
