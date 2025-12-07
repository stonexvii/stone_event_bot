from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

import config


class Membership(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            update: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        bot = update.bot
        membership = await bot.get_chat_member(config.CHANNEL_ID, update.from_user.id)
        if membership.status in {'creator', 'member', 'administrator'}:
            result = await handler(update, data)
            return result
        await bot.send_message(
            chat_id=update.from_user.id,
            text='Для использования бота подпишись на канал автора:\nhttps://t.me/stone_live'
        )
