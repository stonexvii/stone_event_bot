from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.tables import Question
from ..buttons import KeyboardButton
from ..callback_data import CallbackBackButton, CallbackMenu, CallbackQuestion, CallbackGuestAnswer, CallbackPushAnswer, \
    CallbackEvent


def ikb_opinions_menu(question_list: list[Question]):
    keyboard = InlineKeyboardBuilder()
    if question_list:
        event_id = question_list[0].event_id
        for question in question_list:
            keyboard.button(
                **KeyboardButton(question.question, CallbackQuestion, button='question', id=question.id).as_kwargs(),
            )
        keyboard.button(
            **KeyboardButton('Удалить всё!', CallbackEvent, button='delete_questions', event_id=event_id).as_kwargs(),
        )
    keyboard.button(
        **KeyboardButton('Назад', CallbackBackButton, button='back').as_kwargs(),
    )
    keyboard.adjust(*[1] * len(question_list), 2)
    return keyboard.as_markup()


def ikb_question_menu(question_id: int):
    keyboard = InlineKeyboardBuilder()
    buttons = [
        KeyboardButton('Отправить', CallbackQuestion, button='send_question', id=question_id),
        KeyboardButton('Сколько?', CallbackQuestion, button='amount', id=question_id),
        KeyboardButton('Результаты', CallbackQuestion, button='get_result', id=question_id),
        KeyboardButton('Удалить', CallbackQuestion, button='delete_question', id=question_id),
        KeyboardButton('Сбросить', CallbackQuestion, button='reset', id=question_id),
        KeyboardButton('Назад', CallbackMenu, button='opinions_menu'),
    ]
    for button in buttons:
        keyboard.button(
            **button.as_kwargs(),
        )

    keyboard.adjust(3, 2, 1)
    return keyboard.as_markup()


def ikb_guests_answers_admin_menu(question_id: int, answers_list: dict[int, dict[str, str | int]]):
    keyboard = InlineKeyboardBuilder()
    for idx, answer in answers_list.items():
        keyboard.button(
            **KeyboardButton(
                f'{answer['text']}: {answer['amount']}',
                CallbackPushAnswer,
                button='push',
                question_id=question_id,
                answer_id=idx,
            ).as_kwargs()
        )
    keyboard.button(
        **KeyboardButton('К вопросам', CallbackMenu, button='opinions_menu').as_kwargs()
    )
    keyboard.adjust(1)
    return keyboard.as_markup()


def ikb_guest_start_menu(user_tg_id: int):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        **KeyboardButton(
            'Начать!',
            CallbackGuestAnswer,
            user_tg_id=user_tg_id,
        ).as_kwargs()
    )
    return keyboard.as_markup()


def ikb_guest_answer_menu(user_tg_id: int, question: Question):
    keyboard = InlineKeyboardBuilder()
    for answer in question.answers:
        keyboard.button(
            **KeyboardButton(
                answer.answer,
                CallbackGuestAnswer,
                user_tg_id=user_tg_id,
                question_id=question.id,
                answer_id=answer.id,
                answer_list_id=answer.answer_id,
            ).as_kwargs()
        )
    keyboard.adjust(1)
    return keyboard.as_markup()
