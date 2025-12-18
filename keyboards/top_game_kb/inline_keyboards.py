from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..buttons import KeyboardButton
from ..callback_data import CallbackBackButton, CallbackTopGame

NUMBERS = [
    '',
    '1️⃣',
    '2️⃣',
    '3️⃣',
    '4️⃣',
    '5️⃣',
]


def ikb_top_game_answers(dict_message: dict):
    keyboard = InlineKeyboardBuilder()
    for idx, (key, value) in enumerate(dict_message.items()):
        if key != 'question':
            check = '✅ ' if value['visible'] else NUMBERS[idx]
            keyboard.button(
                **KeyboardButton(check + value['text'], CallbackTopGame, button=key).as_kwargs(),
            )
    keyboard.button(
        **KeyboardButton('Назад', CallbackBackButton, button='back').as_kwargs(),
    )
    keyboard.adjust(1)
    return keyboard.as_markup()
