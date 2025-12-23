from datetime import datetime

from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import config
from ai_gpt import ai_client
from ai_gpt import prompts
from ai_gpt.enums import GPTRole
from ai_gpt.gpt_client import GPTMessage
from classes import async_pusher
from classes import current_event
from data import messages
from database import requests
from fsm import TopGame, Events, QuestionForUser, UserSending
from keyboards import ikb_top_game_answers, ikb_guest_answer_menu
from keyboards.callback_data import CallbackGuestAnswer
from utils import FileManager
from utils.bot import get_text_from_message, response_to_dict
from .inline_routers.menu import admin_events_menu

fsm_router = Router()


@fsm_router.message(QuestionForUser.wait_user_answer)
async def disable_user(message: Message, state: FSMContext, bot: Bot):
    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id
    )


@fsm_router.callback_query(QuestionForUser.question_for_user, CallbackGuestAnswer.filter())
async def next_user_question(callback: CallbackQuery, callback_data: CallbackGuestAnswer, state: FSMContext, bot: Bot):
    data = await state.get_data()
    if data:
        question_id = data['question_id']
    else:
        question_id = callback_data.question_id
    await state.update_data({'question_id': question_id + 1})
    if question_id < len(current_event.questions):
        await state.set_state(QuestionForUser.wait_user_answer)
        msg_text = f'Вопрос {question_id + 1} из {len(current_event.questions)}\n\n{current_event.questions[question_id].question}'
        keyboard = ikb_guest_answer_menu(callback_data.user_tg_id, current_event.questions[question_id])
    else:
        msg_text = FileManager.read_txt(messages.USER_FINAL)
        keyboard = None
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=msg_text,
        reply_markup=keyboard,
    )


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


@fsm_router.message(UserSending.wait_for_message)
async def user_sending(message: Message, state: FSMContext, bot: Bot):
    event_id = await state.get_value('event_id')
    users = await requests.get_event_users(event_id)
    successful = 0
    for user in users:
        try:
            await message.copy_to(
                chat_id=user.id,
            )
            await requests.set_user_sending(user.id)
            successful += 1
        except Exception:
            pass
    await state.clear()
    await message.answer(
        text=f'Отправлено {successful}/{len(users)} сообщений!'
    )


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
