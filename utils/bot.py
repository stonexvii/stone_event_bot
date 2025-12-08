import os

from aiogram import Bot
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ai_gpt import ai_client
# from data.generators import get_bot_message
from fsm import Generate
from utils.enums import Path
import json


# async def bot_thinking(message: Message, state: FSMContext, bot: Bot):
#     data = await state.get_state()
#     file_path = 'generate' if data == Generate.wait_for_answer else 'reminder'
#     msg_text = await get_bot_message(file_path)
#     await message.answer(
#         text=msg_text,
#     )
#     await bot.send_chat_action(
#         chat_id=message.from_user.id,
#         action=ChatAction.TYPING,
#     )


async def voice_to_text(message: Message, bot: Bot):
    try:
        voice = await bot.get_file(message.voice.file_id)
        file_path = voice.file_path
        voice_ogg = os.path.join(Path.VOICE.value, f'voice_{message.from_user.id}.ogg')
        await bot.download_file(file_path, destination=voice_ogg)
        response_text = await ai_client.transcript_voice(voice_ogg, bot)
        os.remove(voice_ogg)
        return response_text
    except Exception as e:
        await message.answer(f"⚠️ Ошибка при обработке аудио: {e}")
        return None


async def get_text_from_message(message: Message, bot: Bot):
    if message.voice:
        data_text = await voice_to_text(message, bot)
    else:
        data_text = message.text
    return data_text


def response_to_dict(message_text: str):
    data = json.loads(message_text)
    for key, value in data.items():
        if key != 'question':
            data[key] = {
                'answer': value,
                'visible': False,
            }
    return data


def db_to_dict(questions_list):
    questions = {}
    for question in questions_list:
        questions[str(question.id)] = {
            'question': question.question,
            'answers': {},
        }
        for answer in question.answers:
            questions[str(question.id)]['answers'][str(answer.answer_id)] = answer.answer
    return questions
