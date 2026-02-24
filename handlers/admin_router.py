from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from classes import current_event
from database import requests
from fsm import UserSending
from keyboards.callback_data import CallbackMenu
from middleware import AdminMiddleware
from utils.filemanager import question_from_text

admin_router = Router()
admin_router.message.middleware(AdminMiddleware())


@admin_router.message(F.document)
async def catch_document(message: Message):
    text_file = await message.bot.download(message.document.file_id)
    text = text_file.read().decode("utf-8")
    questions = question_from_text(text)
    for question, *answers in questions:
        await requests.new_question(current_event.id, question, answers)
    await message.answer(
        text=f'{len(questions)} вопросов загружено!'
    )


@admin_router.message(Command('new'))
async def new_question(message: Message, command: CommandObject, bot: Bot):
    question, *answers = command.args.split('\n')
    await requests.new_question(current_event.id, question, answers)
    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id
    )
    await message.answer(
        text=f'Вопрос: {question}\nСоздан!',
    )


@admin_router.message(Command('send', 'sendall'))
async def send_for_users(message: Message, state: FSMContext):
    await state.set_state(UserSending.wait_for_message)
    if not message.text.endswith('all'):
        await state.update_data(event_id=current_event.id)
        msg = f'гостям мероприятия {current_event.title}'
    else:
        msg = 'всем гостям'
    await message.answer(
        text='Пришли сообщение, которое мы отправим ' + msg,
    )


@admin_router.callback_query(CallbackMenu.filter(F.button == 'users_amount'))
async def users_amount(callback: CallbackQuery, bot: Bot, state: FSMContext):
    users = await requests.get_event_users(current_event.id)
    await callback.answer(
        text=f'{len(users)} активных пользователей на этом мероприятии',
        show_alert=True,
    )


@admin_router.message(Command('switch'))
async def switch_users_message(message: Message):
    if current_event.catch_answers:
        current_event.catch_answers = False
        msg = '❌'
    else:
        current_event.catch_answers = True
        msg = '✅'
    await message.answer(
        text='Сообщения гостей: ' + msg
    )
