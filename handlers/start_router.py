from aiogram import Router, Bot
from aiogram.enums import ChatAction
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database import requests
# from database.tables import User
from keyboards import ikb_main_menu
from utils import FileManager
from utils.enums import Path
from middleware import AdminMiddleware, AddAdminArgument

start_router = Router()
start_router.message.middleware(AddAdminArgument())


async def main_menu(message: Message, bot: Bot, state: FSMContext):
    await state.clear()
    await message.answer(
        text='Ты админ!',
        reply_markup=ikb_main_menu(),
    )


@start_router.message(Command('start'))
async def command_start(message: Message, command: CommandObject, admin: bool, bot: Bot, state: FSMContext):
    if admin:
        await main_menu(message, bot, state)
    else:
        event_id = int(command.args)
        await requests.new_user(message.from_user.id, message.from_user.username, event_id)
        await message.answer(
            text='Ты пользователь',
        )

#
#
# async def message_main_menu(message: Message, message_id: int, user: User, state: FSMContext, bot: Bot):
#     await state.clear()
#     msg_text = await FileManager.read(Path.START_COMMAND.value, user_name=user.name)
#     await bot.edit_message_text(
#         chat_id=message.from_user.id,
#         message_id=message_id,
#         text=msg_text,
#         reply_markup=ikb_main_menu(),
#     )
# #
# #
# # @command_router.message(Command('start'))
# # async def command_start(message: Message, user: User, bot: Bot):
# #     if user:
# #         await bot.send_chat_action(
# #             chat_id=message.from_user.id,
# #             action=ChatAction.TYPING,
# #         )
# #         msg_text = await FileManager.read(Path.START_COMMAND.value, user_name=user.name)
# #         keyboard = ikb_main_menu()
# #     else:
# #         msg_text = await FileManager.read(Path.MESSAGE.value, 'welcome_start', user_name=message.from_user.full_name)
# #         keyboard = ikb_welcome('Продолжить', 'apply')
# #     await message.answer(
# #         text=msg_text,
# #         reply_markup=keyboard,
# #     )
