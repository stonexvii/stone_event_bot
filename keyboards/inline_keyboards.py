from aiogram.utils.keyboard import InlineKeyboardBuilder

from .buttons import KeyboardButton
from .callback_data import CallbackBackButton, CallbackTopGame, CallbackMenu, CallbackQuestion, CallbackGuestAnswer, CallbackPushAnswer
from database.tables import Question


def ikb_main_menu():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        KeyboardButton('Ваше мнение', CallbackMenu, button='opinions'),
        KeyboardButton('ТОП-5', CallbackMenu, button='top'),
        KeyboardButton('Мероприятия', CallbackMenu, button='events'),
    ]
    for button in buttons:
        keyboard.button(**button.as_kwargs())
    keyboard.adjust(2, 1)
    return keyboard.as_markup()


def ikb_events_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        **KeyboardButton('Создать', CallbackMenu, button='new_event').as_kwargs(),
    )
    keyboard.button(
        **KeyboardButton('Назад', CallbackBackButton, button='back').as_kwargs(),
    )
    return keyboard.as_markup()


def ikb_cancel_new_event():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        **KeyboardButton('Отмена', CallbackMenu, button='events').as_kwargs(),
    )
    return keyboard.as_markup()


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


def ikb_guests_answers_admin_menu(question_id: str, answers_list: dict):
    keyboard = InlineKeyboardBuilder()
    for idx, answer in sorted(answers_list.items(), key=lambda x: x[1]['amount'], reverse=True):
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
        **KeyboardButton('Назад', CallbackQuestion, button='question', id=question_id).as_kwargs()
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


# def ikb_welcome(text: str, button: str):
#     keyboard = InlineKeyboardBuilder()
#     keyboard.button(**KeyboardButton(text, CallbackMainMenu, button=button).as_kwargs())
#     return keyboard.as_markup()
#
#
# def ikb_approve_button(button: str):
#     keyboard = InlineKeyboardBuilder()
#     button_text = 'Закончить' if button == 'generate' else 'Сохранить'
#     keyboard.button(**KeyboardButton(button_text, CallbackApprove, button=button).as_kwargs())
#     return keyboard.as_markup()
#
#
# def ikb_main_menu():
#     keyboard = InlineKeyboardBuilder()
#     buttons = [
#         KeyboardButton('Поздравление', CallbackMainMenu, button='generate'),
#         KeyboardButton('Напоминание', CallbackMainMenu, button='reminder'),
#     ]
#     for button in buttons:
#         keyboard.button(**button.as_kwargs())
#     keyboard.adjust(2)
#     return keyboard.as_markup()
#
#
# def ikb_remind_menu(task_id: int):
#     keyboard = InlineKeyboardBuilder()
#     buttons = [
#         KeyboardButton('Поздравление', CallbackMainMenu, button='generate', id=task_id),
#         KeyboardButton('Назад', CallbackBackButton, button='to_main'),
#     ]
#     for button in buttons:
#         keyboard.button(**button.as_kwargs())
#     keyboard.adjust(2)
#     return keyboard.as_markup()
#
#
def ikb_back_button():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(**KeyboardButton('Назад', CallbackBackButton, button='to_main').as_kwargs())
    return keyboard.as_markup()
