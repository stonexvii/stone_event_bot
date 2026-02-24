from aiogram import Router, Bot
from aiogram.types import CallbackQuery, Message

import config
from classes import current_event
from database import requests
from keyboards.callback_data import CallbackGuestAnswer

user_router = Router()


@user_router.callback_query(CallbackGuestAnswer.filter())
async def catch_guest_answer(callback: CallbackQuery, callback_data: CallbackGuestAnswer, bot: Bot):
    await requests.add_user_answer(callback.from_user.id, callback_data.question_id, callback_data.answer_id)
    question = current_event.get_question(callback_data.question_id)
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=(f'Спасибо!\nВопрос: {question.question}\nВаш ответ: ' +
              f'{question.answers[callback_data.answer_list_id - 1].answer} - принят!'),
    )


@user_router.message()
async def any_message(message: Message, bot: Bot):
    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id
    )
    if current_event.catch_answers:
        if message.text:
            await bot.send_message(
                chat_id=config.MONITOR_ID,
                text=message.text,
            )
        elif message.photo:
            await bot.send_photo(
                chat_id=config.MONITOR_ID,
                photo=message.photo[-1].file_id,
                caption=message.caption
            )
