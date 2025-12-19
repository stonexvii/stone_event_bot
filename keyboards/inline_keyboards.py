from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.tables import Event
from .buttons import KeyboardButton
from .callback_data import CallbackBackButton, CallbackMenu, CallbackEvent


def ikb_main_menu():
    keyboard = InlineKeyboardBuilder()
    buttons = [
        KeyboardButton('Ваше мнение', CallbackMenu, button='opinions_menu'),
        KeyboardButton('ТОП-5', CallbackMenu, button='top'),
        KeyboardButton('Мероприятия', CallbackMenu, button='events'),
    ]
    for button in buttons:
        keyboard.button(**button.as_kwargs())
    keyboard.adjust(2, 1)
    return keyboard.as_markup()


def ikb_select_event(events_list: list[Event]):
    keyboard = InlineKeyboardBuilder()
    buttons = [
        KeyboardButton('Создать', CallbackMenu, button='new_event'),
        KeyboardButton('Назад', CallbackBackButton, button='back')
    ]
    for event in events_list:
        keyboard.button(
            **KeyboardButton(
                f'{event.date} {event.title}',
                CallbackEvent,
                button='target_event',
                event_id=event.id,
            ).as_kwargs(),
        )
    for button in buttons:
        keyboard.button(**button.as_kwargs())
    keyboard.adjust(*[1] * (len(events_list)), 2)
    return keyboard.as_markup()


def ikb_events_menu(events_list: list[Event]):
    keyboard = InlineKeyboardBuilder()
    buttons = [
        KeyboardButton('Создать', CallbackMenu, button='new_event'),
        KeyboardButton('Назад', CallbackBackButton, button='back')
    ]
    for event in sorted(events_list, key=lambda item: item.date):
        keyboard.button(
            **KeyboardButton(
                f'{event.date} {event.title}' + (' ✅' if event.active else ''),
                CallbackEvent,
                button='select',
                event_id=event.id,
            ).as_kwargs(),
        )
    for button in buttons:
        keyboard.button(**button.as_kwargs())
    keyboard.adjust(*[1] * (len(events_list)), 2)
    return keyboard.as_markup()


def ikb_cancel_new_event():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        **KeyboardButton('Отмена', CallbackMenu, button='events').as_kwargs(),
    )
    return keyboard.as_markup()


def ikb_event_menu(event: Event):
    keyboard = InlineKeyboardBuilder()
    buttons = [
        KeyboardButton('Активировать', CallbackEvent, button='activate', event_id=event.id),
        KeyboardButton('Заголовок', CallbackEvent, button='title', event_id=event.id),
        KeyboardButton('Закончить', CallbackEvent, button='done', event_id=event.id),
        KeyboardButton('Назад', CallbackMenu, button='events'),
    ]
    for button in buttons:
        keyboard.button(**button.as_kwargs())
    keyboard.adjust(1)
    return keyboard.as_markup()


def ikb_back_button():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(**KeyboardButton('Назад', CallbackBackButton, button='to_main').as_kwargs())
    return keyboard.as_markup()
