from aiogram import Router, Bot, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message,BufferedInputFile

from middleware import AdminMiddleware
from utils import FileManager
from utils.enums import Path
from utils.filemanager import question_from_text
from database import requests
import asyncio
import aiohttp
from io import BytesIO
from aiogram import Bot, Dispatcher, types
from async_apps import qr_code_app

admin_router = Router()
admin_router.message.middleware(AdminMiddleware())



@admin_router.message(F.document)
async def catch_document(message: Message, bot: Bot):
    text_file = await message.bot.download(message.document.file_id)
    text = text_file.read().decode("utf-8")
    questions = question_from_text(text)
    for question, *answers in questions:
        await requests.new_question(question, answers)
    await message.answer(
        text=f'{len(questions)} вопросов загружено!'
    )
