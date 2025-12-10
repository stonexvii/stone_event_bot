from aiogram import Router, Bot
from aiogram.types import CallbackQuery

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
        text=f'Спасибо!\nВопрос: {question.question}\nВаш ответ: {question.answers[callback_data.answer_id - 1].answer} - принят!'
    )
