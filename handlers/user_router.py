from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from classes import current_event
from database import requests
from fsm import QuestionForUser
from keyboards.callback_data import CallbackGuestAnswer
# from .fsm_routers import next_user_question
from utils.bot import voice_to_text
from ai_gpt import ai_client
from ai_gpt.gpt_message import GPTMessage
from ai_gpt.prompts import TOAST, SIMPLE_TOAST
from ai_gpt.enums import GPTRole
from keyboards import ikb_make_toast
from keyboards.callback_data import CallbackMenu

user_router = Router()


# @user_router.callback_query(CallbackGuestAnswer.filter())
# async def catch_guest_answer(callback: CallbackQuery, callback_data: CallbackGuestAnswer, state: FSMContext, bot: Bot):
#     await requests.add_user_answer(callback.from_user.id, callback_data.question_id, callback_data.answer_id)
#     question = current_event.get_question(callback_data.question_id)
#     # await callback.answer(
#     #     text=f'Спасибо!\nВопрос: {question.question}\nВаш ответ: {question.answers[callback_data.answer_list_id - 1].answer} - принят!',
#     #     show_alert=True,
#     # )
#     await bot.edit_message_text(
#         chat_id=callback.from_user.id,
#         message_id=callback.message.message_id,
#         text=f'Спасибо!\nВопрос: {question.question}\nВаш ответ: {question.answers[callback_data.answer_list_id - 1].answer} - принят!',
#     )
#     # await next_user_question(callback, callback_data, state, bot)


# @user_router.message()
# async def disable_user(message: Message, state: FSMContext, bot: Bot):
#
#     await bot.delete_message(
#         chat_id=message.from_user.id,
#         message_id=message.message_id
#     )

@user_router.callback_query(CallbackMenu.filter(F.button == 'make_toast'))
async def make_toast(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.send_message(
        chat_id=callback.from_user.id,
        text='Сейчас подумаем, что можно предложить',
    )
    message_text = GPTMessage(SIMPLE_TOAST)
    response = await ai_client.request(message_text, bot)

    await bot.send_message(
        chat_id=callback.from_user.id,
        text=response,
        reply_markup=ikb_make_toast(),
    )


@user_router.message()
async def user_message(message: Message, bot: Bot):
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Сейчас подумаем, что можно предложить',
    )
    message_text = await voice_to_text(message, bot)
    message_list = GPTMessage(TOAST)
    message_list.update(GPTRole.USER, message_text)
    response = await ai_client.request(message_list, bot)
    await message.answer(
        text=response,
        reply_markup=ikb_make_toast(),
    )
