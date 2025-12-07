from datetime import date
from datetime import datetime
from asyncio import sleep
from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from ai_gpt import GPTMessage
from ai_gpt.enums import GPTRole
# from data import get_examples
# from database import requests
# from database.tables import User
from fsm import Generate, Reminder, TopGame
from keyboards import ikb_top_game_answers, ikb_back_button, ikb_main_menu
# from keyboards.callback_data import CallbackBackButton, CallbackMainMenu, CallbackApprove
# from scheduler.scheduler import schedule_event
from utils import FileManager
from utils.enums import Path
from keyboards.callback_data import CallbackTopGame, CallbackMenu, CallbackBackButton
from middleware import AdminMiddleware

callback_router = Router()
callback_router.callback_query.middleware(AdminMiddleware())


async def main_menu(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text='Работаю',
        reply_markup=ikb_main_menu(),
    )


@callback_router.callback_query(CallbackBackButton.filter())
async def back_to_main_menu(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await main_menu(callback, bot, state)


@callback_router.callback_query(CallbackMenu.filter(F.button == 'top'))
async def start_top_game(callback: CallbackQuery, callback_data: CallbackMenu, bot: Bot, state: FSMContext):
    await state.set_state(TopGame.wait_for_request)
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text='Задавай тему для игры',
        reply_markup=ikb_back_button(),

    )


@callback_router.callback_query(CallbackTopGame.filter(), TopGame.show_answers)
async def top_game_answer(callback: CallbackQuery, callback_data: CallbackTopGame, state: FSMContext, bot: Bot):
    # msg_text = await FileManager.read(Path.START_COMMAND.value, user_name=user.name)
    await callback.answer(
        text='',
    )
    message_data = await state.get_data()
    message_data[callback_data.button]['visible'] = True
    await state.update_data(
        **message_data,
    )
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=message_data['question'],
        reply_markup=ikb_top_game_answers(message_data),
    )
#
#
# async def callback_main_menu(callback: CallbackQuery, user: User, state: FSMContext, bot: Bot):
#     await state.clear()
#     msg_text = await FileManager.read(Path.START_COMMAND.value, user_name=user.name)
#     await bot.edit_message_text(
#         chat_id=callback.from_user.id,
#         message_id=callback.message.message_id,
#         text=msg_text,
#         reply_markup=ikb_main_menu(),
#     )
#
#
# @callback_router.callback_query(CallbackMainMenu.filter(F.button == 'apply'))
# async def apply_welcome(callback: CallbackQuery, state: FSMContext, bot: Bot):
#     msg_text = await FileManager.read(Path.MESSAGE.value, 'welcome_name', user_name=callback.from_user.full_name)
#     await requests.new_user(
#         user_tg_id=callback.from_user.id,
#         name=callback.from_user.full_name,
#         tg_username=callback.from_user.username,
#     )
#     await bot.edit_message_text(
#         chat_id=callback.from_user.id,
#         message_id=callback.message.message_id,
#         text=msg_text,
#         reply_markup=ikb_welcome('Пропустить', 'skip'),
#     )
#     await state.set_state(UserName.wait_for_answer)
#     await state.update_data(
#         {
#             'message_id': callback.message.message_id,
#         }
#     )
#
#
# @callback_router.callback_query(CallbackMainMenu.filter(F.button == 'skip'))
# async def skip_name(callback: CallbackQuery, user: User, state: FSMContext, bot: Bot):
#     await callback_main_menu(callback, user, state, bot)
#
#
# @callback_router.callback_query(CallbackMainMenu.filter())
# async def menu_item(callback: CallbackQuery, callback_data: CallbackMainMenu, user: User, state: FSMContext, bot: Bot):
#     examples = await get_examples(callback_data.button)
#     msg_text = await FileManager.read(Path.MESSAGE.value, f'start_{callback_data.button}', user_name=user.name,
#                                       examples=examples)
#     await bot.edit_message_text(
#         chat_id=callback.from_user.id,
#         message_id=callback.message.message_id,
#         text=msg_text,
#         reply_markup=ikb_back_button(),
#     )
#     state_name = Generate
#     if callback_data.button == 'reminder':
#         state_name = Reminder
#     await state.set_state(state_name.wait_for_answer)
#     msg_list = GPTMessage(callback_data.button)
#     add_task = ''
#     if idx := callback_data.id:
#         task = await requests.get_task(idx)
#         add_task = f'\nПоздравь {task.name} с {task.event_type}'
#     msg_list.update(GPTRole.USER, f'Привет, меня зовут {user.name}!' + add_task)
#     await state.update_data({'messages': msg_list.json()})
#
#
# @callback_router.callback_query(CallbackBackButton.filter(F.button == 'to_main'))
# async def back_to_main_menu(callback: CallbackQuery, user: User, state: FSMContext, bot: Bot):
#     await callback_main_menu(callback, user, state, bot)
#
#
# @callback_router.callback_query(CallbackApprove.filter())
# async def approve_callback(callback: CallbackQuery, callback_data: CallbackApprove, user: User, state: FSMContext,
#                            bot: Bot):
#     if callback_data.button == 'generate':
#         msg_text = 'Супер!\nИстория нашей переписки очищена'
#         await bot.send_message(
#             chat_id=callback.from_user.id,
#             text=callback.message.text.split('\n\n', 1)[1].rsplit('\n\n', 1)[0],
#         )
#     else:
#         msg_text = 'Отлично!\nЯ записал уведомление и оповещу тебя как и договорились!'
#         json_data = await state.get_value('json')
#         reminder = datetime.fromisoformat(json_data['reminder'])
#         event_date = date.fromisoformat(json_data['date'])
#         task = await requests.new_task(
#             user_tg_id=callback.from_user.id,
#             user_name=user.name,
#             event_type=json_data['event'],
#             event_date=event_date,
#             reminder=reminder,
#         )
#         data = {
#             'task_id': task.id,
#             'user_name': user.name,
#             'name': json_data['name'],
#             'event': json_data['event'],
#             'date': event_date,
#             'reminder': reminder,
#         }
#         schedule_event(callback.from_user.id, data, bot)
#     await callback.answer(
#         text=msg_text,
#         show_alert=True,
#     )
#     await sleep(3)
#     await new_main_menu(callback, user, state, bot)
