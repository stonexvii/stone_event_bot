from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from database import requests
from middleware import AdminMiddleware
from utils.filemanager import question_from_text
from classes import current_event
from fsm import UserSending

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


@admin_router.message(Command('send'))
async def send_for_users(message: Message, command: CommandObject, state: FSMContext):
    if command.args.isdigit():
        event_id = int(command.args)
        await state.set_state(UserSending.wait_for_message)
        await state.update_data(event_id=event_id)
        await message.answer(
            text='Пришли сообщение, которое мы отправим людям'
        )

    # text_file = await message.bot.download(message.document.file_id)
    # text = text_file.read().decode("utf-8")
    # questions = question_from_text(text)
    # for question, *answers in questions:
    #     await requests.new_question(current_event.id, question, answers)
    # await message.answer(
    #     text=f'{len(questions)} вопросов загружено!'
    # )
