from datetime import datetime

from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ai_gpt import ai_client
from ai_gpt import prompts
from ai_gpt.enums import GPTRole
from ai_gpt.gpt_client import GPTMessage
from classes import async_pusher
from database import requests
from fsm import TopGame, Events
from keyboards import ikb_top_game_answers
from utils.bot import get_text_from_message, response_to_dict
from .inline_routers.menu import admin_events_menu

fsm_router = Router()


@fsm_router.message(Events.new_event)
async def catch_new_event(message: Message, bot: Bot, state: FSMContext):
    description, str_date = message.text.rsplit(' ', 1)
    event_date = datetime.strptime(str_date, '%Y/%m/%d')
    await requests.new_event(description, event_date)
    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id,
    )
    await admin_events_menu(message, bot, state)


@fsm_router.message(TopGame.wait_for_request)
async def catch_voice_message(message: Message, bot: Bot, state: FSMContext):
    msg_text = await get_text_from_message(message, bot)
    if msg_text:
        msg_list = GPTMessage(prompts.TOP_GAME)
        msg_list.update(GPTRole.USER, msg_text)
        response = await ai_client.request(msg_list, bot)
        message_data = response_to_dict(response)
        await async_pusher.set_top5(**message_data)
        await state.update_data(
            **message_data,
        )
        await state.set_state(TopGame.show_answers)
        await message.answer(
            text=message_data['question'],
            reply_markup=ikb_top_game_answers(message_data),
        )


@fsm_router.message(Events.set_title)
async def catch_event_title(message: Message, bot: Bot, state: FSMContext):
    event_id = await state.get_value('event_id')
    await requests.title_event(event_id, message.text)
    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id,
    )
    await admin_events_menu(message, bot, state)
