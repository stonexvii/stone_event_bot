from aiogram import Router

from .menu import menu_router
from .opinions_router import opinions_router
from .top_game_router import top_game_router

inline_router = Router()

inline_router.include_routers(
    opinions_router,
    top_game_router,
    menu_router,
)
