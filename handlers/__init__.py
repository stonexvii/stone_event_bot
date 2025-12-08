from aiogram import Router

# from middleware import Membership, UserMiddleware
from .admin_router import admin_router
from .callback_router import callback_router
from .start_router import start_router
from .user_router import user_router
from .fsm_routers import fsm_router
from .inline_routers import inline_router

bot_main_router = Router()
# bot_main_router.message.middleware(Membership())
# bot_main_router.message.middleware(UserMiddleware())
# bot_main_router.callback_query.middleware(Membership())
# bot_main_router.callback_query.middleware(UserMiddleware())

bot_main_router.include_routers(
    admin_router,
    start_router,
    inline_router,
    fsm_router,
    user_router,
)
