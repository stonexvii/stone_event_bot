from aiogram import Router

from .admin_router import admin_router
from .fsm_routers import fsm_router
from .inline_routers import inline_router
from .start_router import start_router
from .user_router import user_router

bot_main_router = Router()

bot_main_router.include_routers(
    fsm_router,
    admin_router,
    start_router,
    inline_router,
    user_router,
)
