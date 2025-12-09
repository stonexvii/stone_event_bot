from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..buttons import KeyboardButton
from ..callback_data import CallbackBackButton, CallbackTopGame, CallbackMenu, CallbackQuestion, CallbackGuestAnswer, CallbackPushAnswer
from database.tables import Question

def ikb_top_game_answers(dict_message: dict):
    keyboard = InlineKeyboardBuilder()
    for key, value in dict_message.items():
        if key != 'question':
            check = '✅ ' if value['visible'] else ''
            keyboard.button(
                **KeyboardButton(check + value['answer'], CallbackTopGame, button=key).as_kwargs(),
            )
    keyboard.button(
        **KeyboardButton('Назад', CallbackBackButton, button='back').as_kwargs(),
    )
    keyboard.adjust(1)
    return keyboard.as_markup()