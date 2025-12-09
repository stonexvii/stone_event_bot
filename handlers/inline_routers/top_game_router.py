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
from async_apps import async_pusher

top_game_router = Router()
top_game_router.callback_query.middleware(AdminMiddleware())


@top_game_router.callback_query(CallbackMenu.filter(F.button == 'top'))
async def start_top_game(callback: CallbackQuery, callback_data: CallbackMenu, bot: Bot, state: FSMContext):
    await state.set_state(TopGame.wait_for_request)
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text='Задавай тему для игры',
        reply_markup=ikb_back_button(),

    )


@top_game_router.callback_query(CallbackTopGame.filter(), TopGame.show_answers)
async def top_game_answer(callback: CallbackQuery, callback_data: CallbackTopGame, state: FSMContext, bot: Bot):
    await callback.answer(
        text='',
    )
    message_data = await state.get_data()
    message_data[callback_data.button]['visible'] = True
    await state.update_data(
        **message_data,
    )
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=message_data['question'],
        reply_markup=ikb_top_game_answers(message_data),
    )
