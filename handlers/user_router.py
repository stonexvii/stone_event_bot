import json

from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from ai_gpt import ai_client
from ai_gpt.enums import GPTRole
from ai_gpt.gpt_client import GPTMessage
# from database import requests
# from database.tables import User
from fsm import Generate, Reminder, UserName
from keyboards import ikb_back_button
from keyboards.callback_data import CallbackGuestAnswer
from utils import FileManager
from utils.bot import get_text_from_message
from utils.enums import Path
from database import requests

# from .command import message_main_menu

user_router = Router()


@user_router.callback_query(CallbackGuestAnswer.filter())
async def catch_guest_answer(callback: CallbackQuery, callback_data: CallbackGuestAnswer, bot: Bot):
    await requests.add_guest_answer(callback.from_user.id, int(callback_data.question_id), int(callback_data.answer_id))
    question = await requests.get_question(int(callback_data.question_id))
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=f'Спасибо!\nВопрос: {question.question}\nВаш ответ: {question.answers[int(callback_data.answer_id)-1].answer} - принят!'
    )
    # await callback.answer(
    #     text=f'{callback_data.user_tg_id} {callback_data.question_id} {callback_data.answer_id}'
    # )
# @user_router.message(Command('start'))
# async def command_start(message: Message, bot: Bot, state: FSMContext):
#     await bot.send_message(
#         chat_id=message.from_user.id,
#         text='Ты пользователь',
#     )
# await bot.delete_message(
#     chat_id=message.from_user.id,
#     message_id=message.message_id,
# )
# await message_main_menu(message, message_id, user, state, bot)
#
#
# @user_router.message(Generate.wait_for_answer)
# @user_router.message(Reminder.wait_for_answer)
# async def wait_for_answer(message: Message, bot: Bot, state: FSMContext):
#     await bot_thinking(message, state, bot)
#     msg_text = await get_text_from_message(message, bot)
#     if msg_text:
#         data = await state.get_value('messages')
#         msg_list = GPTMessage.from_json(data)
#         msg_list.update(GPTRole.USER, msg_text)
#         response = await ai_client.request(msg_list, bot)
#         keyboard = ikb_back_button()
#         if response.startswith('INCORRECT'):
#             response = response.split('\n', 1)[-1].strip()
#         elif response.startswith('DONE'):
#             response = response.split('\n', 1)[-1].strip()
#             data = json.loads('{' + response + '}')
#             response = await FileManager.read(Path.MESSAGE.value, 'reminder_text', **data)
#             await state.update_data({'json': data})
#             keyboard = ikb_approve_button('reminder')
#         else:
#             msg_list.update(GPTRole.CHAT, response)
#             keyboard = ikb_approve_button('generate')
#         await message.answer(
#             text=response,
#             reply_markup=keyboard,
#         )
#         await state.update_data(
#             {
#                 'messages': msg_list.json(),
#             }
#         )
