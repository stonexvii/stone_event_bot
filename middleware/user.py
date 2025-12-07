# from typing import Callable, Dict, Any, Awaitable
#
# from aiogram import BaseMiddleware
# from aiogram.types import TelegramObject
#
# from database import requests
#
#
# class UserMiddleware(BaseMiddleware):
#     async def __call__(
#             self,
#             handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
#             update: TelegramObject,
#             data: Dict[str, Any]
#     ) -> Any:
#         user = await requests.get_user(update.from_user.id)
#         data['user'] = user
#         result = await handler(update, data)
#         return result
