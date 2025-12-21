from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from classes import async_pusher
from classes.messages import PusherMessage
from fsm import TopGame
from keyboards import *
from keyboards.callback_data import CallbackTopGame, CallbackMenu
from middleware import AdminMiddleware
from utils import FileManager
from data import messages

top_game_router = Router()
top_game_router.callback_query.middleware(AdminMiddleware())


@top_game_router.callback_query(CallbackMenu.filter(F.button == 'top'))
async def start_top_game(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(TopGame.wait_for_request)
    async_pusher.set_message(PusherMessage(5))
    async_pusher.set_title('ТОП 5 против ИИ')
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=FileManager.read_txt(messages.TOP_5_EXAMPLES),
        reply_markup=ikb_back_button(),

    )


@top_game_router.callback_query(CallbackTopGame.filter(), TopGame.show_answers)
async def top_game_answer(callback: CallbackQuery, callback_data: CallbackTopGame, state: FSMContext, bot: Bot):
    await callback.answer(
        text='',
    )
    message_data = await state.get_data()
    message_data[callback_data.button]['visible'] = True
    await async_pusher.set_top5(**message_data)
    await state.update_data(
        **message_data,
    )
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=message_data['question'],
        reply_markup=ikb_top_game_answers(message_data),
    )
