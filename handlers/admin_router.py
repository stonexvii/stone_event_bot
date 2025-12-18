from aiogram import Router, F
from aiogram.types import Message

from database import requests
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
        await requests.new_question(question, answers)
    await message.answer(
        text=f'{len(questions)} вопросов загружено!'
    )
