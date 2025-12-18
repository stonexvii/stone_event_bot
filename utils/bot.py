import json
import os

from aiogram import Bot
from aiogram.types import Message

from ai_gpt import ai_client
from utils.enums import Path


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


def response_to_dict(message_text: str) -> dict[str, str | dict[str, bool | str]]:
    data = json.loads(message_text)
    for key, value in data.items():
        if key != 'question':
            data[key] = {
                'text': value,
                'visible': False,
            }
    return data
