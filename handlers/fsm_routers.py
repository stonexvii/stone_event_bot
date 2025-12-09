import json

from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ai_gpt import ai_client
from ai_gpt.enums import GPTRole
from ai_gpt.gpt_client import GPTMessage
from fsm import TopGame, Events
from keyboards import ikb_top_game_answers
from utils import FileManager
from utils.bot import get_text_from_message, response_to_dict
from utils.enums import Path
# from .command import message_main_menu
from utils.enums import Path
from datetime import datetime
from database import requests
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
        msg_list = GPTMessage(Path.MAIN_PROMPT.value)
        msg_list.update(GPTRole.USER, msg_text)
        response = await ai_client.request(msg_list, bot)
        await message.answer(
            text=response,
        )
        message_data = response_to_dict(response)
        await state.update_data(
            **message_data,
        )
        await state.set_state(TopGame.show_answers)
        await message.answer(
            text=message_data['question'],
            reply_markup=ikb_top_game_answers(message_data),
        )
        # keyboard = ikb_back_button()
        # if response.startswith('INCORRECT'):
        #     response = response.split('\n', 1)[-1].strip()
        # elif response.startswith('DONE'):
        #     response = response.split('\n', 1)[-1].strip()
        #     data = json.loads('{' + response + '}')
        #     response = await FileManager.read(Path.MESSAGE.value, 'reminder_text', **data)
        #     await state.update_data({'json': data})
        #     keyboard = ikb_approve_button('reminder')
        # else:
        #     msg_list.update(GPTRole.CHAT, response)
        #     keyboard = ikb_approve_button('generate')
        # await message.answer(
        #     text=response,
        #     reply_markup=keyboard,
        # )
        # await state.update_data(
        #     {
        #         'messages': msg_list.json(),
        #     }
        # )
