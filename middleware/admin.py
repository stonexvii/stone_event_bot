from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

import config


class AddAdminArgument(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            update: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        data['admin'] = update.from_user.id == config.ADMIN_ID
        result = await handler(update, data)
        return result


class AdminMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            update: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        if update.from_user.id == config.ADMIN_ID:
            result = await handler(update, data)
            return result
