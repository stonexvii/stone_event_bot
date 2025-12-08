from datetime import date
from datetime import datetime
from asyncio import sleep
from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from ai_gpt import GPTMessage
from ai_gpt.enums import GPTRole
# from data import get_examples
# from database import requests
# from database.tables import User
from fsm import Generate, Reminder, TopGame, Events
from keyboards import *
# from keyboards.callback_data import CallbackBackButton, CallbackMainMenu, CallbackApprove
# from scheduler.scheduler import schedule_event
from utils import FileManager
from utils.enums import Path
from utils.bot import db_to_dict
from keyboards.callback_data import CallbackTopGame, CallbackMenu, CallbackBackButton, CallbackQuestion, \
    CallbackPushAnswer
from middleware import AdminMiddleware
from database import requests
from pusher_app import async_pusher


async def main_menu(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text='Работаю',
        reply_markup=ikb_main_menu(),
    )


async def admin_events_menu(update: Message | CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    events = await requests.get_events()
    if events:
        msg_text = '\n'.join([f'{line.id}. ({line.date}) {line.description}' for line in events])
    else:
        msg_text = 'У тебя нет мероприятий'
    message_id = data['message_id'] if isinstance(update, Message) else update.message.message_id
    await bot.edit_message_text(
        chat_id=update.from_user.id,
        message_id=message_id,
        text=msg_text,
        reply_markup=ikb_events_menu(),
    )