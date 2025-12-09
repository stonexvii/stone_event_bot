from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..buttons import KeyboardButton
from ..callback_data import CallbackBackButton, CallbackTopGame, CallbackMenu, CallbackQuestion, CallbackGuestAnswer, CallbackPushAnswer
from database.tables import Question


def ikb_opinions_menu(question_list: dict):
    keyboard = InlineKeyboardBuilder()
    for idx, question in question_list.items():
        keyboard.button(
            **KeyboardButton(question['question'], CallbackQuestion, button='question', id=idx).as_kwargs(),
        )
    keyboard.button(
        **KeyboardButton('Удалить всё!', CallbackMenu, button='delete_all').as_kwargs(),
    )
    keyboard.button(
        **KeyboardButton('Назад', CallbackBackButton, button='back').as_kwargs(),
    )
    keyboard.adjust(*[1] * len(question_list), 2)
    return keyboard.as_markup()


def ikb_question_menu(question_id: str):
    keyboard = InlineKeyboardBuilder()
    buttons = [
        KeyboardButton('Отправить', CallbackQuestion, button='send_question', id=question_id),
        KeyboardButton('Сколько?', CallbackQuestion, button='amount', id=question_id),
        KeyboardButton('Результаты', CallbackQuestion, button='get_result', id=question_id),
        KeyboardButton('Удалить', CallbackQuestion, button='delete_question', id=question_id),
        KeyboardButton('Сбросить', CallbackQuestion, button='reset', id=question_id),
        KeyboardButton('Назад', CallbackMenu, button='opinions'),
    ]
    for button in buttons:
        keyboard.button(
            **button.as_kwargs(),
        )

    keyboard.adjust(3, 2, 1)
    return keyboard.as_markup()


def ikb_guests_answers_admin_menu(question_id: str, answers_list: dict[int, dict[str, str|int]]):
    keyboard = InlineKeyboardBuilder()
    for idx, answer in answers_list.items():
        keyboard.button(
            **KeyboardButton(
                f'{answer['answer']}: {answer['amount']}',
                CallbackPushAnswer,
                button='push',
                question_id=question_id,
                answer_id=idx,
            ).as_kwargs()
        )
    keyboard.button(
        **KeyboardButton('К вопросам', CallbackMenu, button='opinions').as_kwargs()
    )
    keyboard.adjust(1)
    return keyboard.as_markup()


def ikb_guest_answer_menu(user_tg_id: int, question_id: str, answers_list: dict[str, str]):
    keyboard = InlineKeyboardBuilder()
    for idx, answer in answers_list.items():
        keyboard.button(
            **KeyboardButton(
                answer,
                CallbackGuestAnswer,
                user_tg_id=user_tg_id,
                question_id=question_id,
                answer_id=idx,
            ).as_kwargs()
        )
    keyboard.adjust(1)
    return keyboard.as_markup()