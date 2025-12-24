from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from classes import async_pusher
from classes.messages import PusherMessage
from database import requests
from fsm import Events
from keyboards import *
from keyboards.callback_data import CallbackMenu, CallbackEvent
from middleware import AdminMiddleware
from classes import current_event

from ai_gpt import ai_client
from ai_gpt.gpt_message import GPTMessage
from ai_gpt.prompts import SIMPLE_TOAST

menu_router = Router()
menu_router.callback_query.middleware(AdminMiddleware())





async def main_menu(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text='Работаю',
        reply_markup=ikb_main_menu(),
    )


async def admin_events_menu(update: Message | CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    events = await requests.get_events()
    if events:
        msg_text = '\n'.join([f'{line.id}. ({line.date}) {line.description}' for line in events])
    else:
        msg_text = 'У тебя нет мероприятий'
    message_id = data['message_id'] if isinstance(update, Message) else update.message.message_id
    await bot.edit_message_text(
        chat_id=update.from_user.id,
        message_id=message_id,
        text=msg_text,
        reply_markup=ikb_events_menu(events),
    )


@menu_router.callback_query(CallbackMenu.filter(F.button == 'events'))
async def admin_events(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    await admin_events_menu(callback, bot, state)


@menu_router.callback_query(CallbackEvent.filter(F.button == 'select'))
async def select_event(callback: CallbackQuery, callback_data: CallbackEvent, bot: Bot):
    event = await requests.get_event(callback_data.event_id)
    message_text = f'{event.date}\nЗаголовок: {event.title}\n\n{event.description}'
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=message_text,
        reply_markup=ikb_event_menu(event),
    )


@menu_router.callback_query(CallbackEvent.filter(F.button == 'activate'))
async def activate_event(callback: CallbackQuery, callback_data: CallbackEvent, bot: Bot):
    # await requests.activate_event(callback_data.event_id)
    await requests.activate_event(callback_data.event_id)
    await current_event.activate()
    await callback.answer(
        text=f'Активное событие:\n{current_event.title}',
        show_alert=True,
    )
    async_pusher.set_message(PusherMessage(4))
    async_pusher.set_title(current_event.title)

    # img_bytes = await qr_code_app.get_qr(event.id)
    # photo = BufferedInputFile(img_bytes, filename="qr.png")
    # await bot.send_photo(
    #     chat_id=callback.from_user.id,
    #     photo=photo,
    #     caption=f"Вот твой QR 👇",
    # )


@menu_router.callback_query(CallbackEvent.filter(F.button == 'title'))
async def set_event_title(callback: CallbackQuery, callback_data: CallbackEvent, bot: Bot, state: FSMContext):
    await state.set_state(Events.set_title)
    await state.update_data(
        {
            'event_id': callback_data.event_id,
            'message_id': callback.message.message_id,
        },
    )
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text='Введите заголовок для мероприятия:',
    )


@menu_router.callback_query(CallbackEvent.filter(F.button == 'done'))
async def done_event(callback: CallbackQuery, callback_data: CallbackEvent, bot: Bot):
    event = await requests.get_event(callback_data.event_id)
    await requests.done_event(event.id)
    await callback.answer(
        text=f'Событие завершено:\n{event.title}',
        show_alert=True,
    )
