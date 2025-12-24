from aiogram import Router, Bot
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import config
from classes import current_event
from data import messages
from database import requests
from fsm import QuestionForUser
from keyboards import ikb_main_menu, ikb_guest_start_menu, ikb_make_toast
from middleware import AddAdminArgument
from utils import FileManager

start_router = Router()
start_router.message.middleware(AddAdminArgument())


async def main_menu(message: Message, bot: Bot, state: FSMContext):
    await state.clear()
    await message.answer(
        text=FileManager.read_txt(messages.ADMIN_WELCOME),
        reply_markup=ikb_main_menu(),
    )


@start_router.message(Command('start'))
async def command_start(message: Message, command: CommandObject, admin: bool, bot: Bot, state: FSMContext):
    if admin:
        await main_menu(message, bot, state)
    else:
        if command.args:
            event_id = int(command.args)
            events = await requests.get_events()
            if event_id in {event.id for event in events}:
                await requests.new_user(message.from_user.id, message.from_user.username, event_id)
                await message.answer(
                    text=FileManager.read_txt(messages.USER_WELCOME),
                )

            else:
                await bot.send_message(
                    chat_id=config.ADMIN_ID,
                    text='Кто-то лезет с левым ID'
                )
        else:
            if current_event.id:
                # await state.set_state(QuestionForUser.question_for_user)
                user = await requests.new_user(message.from_user.id, message.from_user.username, current_event.id)
                await message.answer(
                    text=FileManager.read_txt(messages.USER_WELCOME),
                    reply_markup=ikb_make_toast(),
                    # reply_markup=ikb_guest_start_menu(message.from_user.id),
                )
