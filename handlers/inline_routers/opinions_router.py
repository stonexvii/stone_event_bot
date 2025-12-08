from datetime import date
from datetime import datetime
from asyncio import sleep
from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from ai_gpt import GPTMessage
from ai_gpt.enums import GPTRole
# from data import get_examples
# from database import requests
# from database.tables import User
from fsm import Generate, Reminder, TopGame, Events
from keyboards import *
# from keyboards.callback_data import CallbackBackButton, CallbackMainMenu, CallbackApprove
# from scheduler.scheduler import schedule_event
from utils import FileManager
from utils.enums import Path
from utils.bot import db_to_dict
from keyboards.callback_data import CallbackTopGame, CallbackMenu, CallbackBackButton, CallbackQuestion, \
    CallbackPushAnswer
from middleware import AdminMiddleware
from database import requests
from pusher_app import async_pusher
from .menu import main_menu, admin_events_menu

opinions_router = Router()
opinions_router.callback_query.middleware(AdminMiddleware())


@opinions_router.callback_query(CallbackBackButton.filter())
async def back_to_main_menu(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await main_menu(callback, bot, state)


@opinions_router.callback_query(CallbackMenu.filter(F.button == 'events'))
async def admin_events(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    await admin_events_menu(callback, bot, state)


@opinions_router.callback_query(CallbackMenu.filter(F.button == 'new_event'))
async def new_event(callback: CallbackQuery, callback_data: CallbackMenu, bot: Bot, state: FSMContext):
    await state.set_state(Events.new_event)
    await state.update_data({'message_id': callback.message.message_id})
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text='Введите: Описание мероприятия YYYY/MM/DD',
        reply_markup=ikb_cancel_new_event(),
    )


@opinions_router.callback_query(CallbackMenu.filter(F.button == 'delete_all'))
async def delete_all_questions(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await requests.delete_questions()
    await callback.answer(
        text='Все вопросы удалены!',
        show_alert=True,
    )


@opinions_router.callback_query(CallbackMenu.filter(F.button == 'opinions'))
async def start_opinions(callback: CallbackQuery, state: FSMContext, bot: Bot):
    questions = await requests.all_questions()
    questions = db_to_dict(questions)
    await async_pusher.trigger()
    await state.update_data(**questions)
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text='Вопросы',
        reply_markup=ikb_opinions_menu(questions),
    )


@opinions_router.callback_query(CallbackQuestion.filter(F.button == 'send_question'))
async def send_question(callback: CallbackQuery, callback_data: CallbackQuestion, bot: Bot, state: FSMContext):
    data = await state.get_data()
    guests = await requests.all_guests()
    question = data[callback_data.id]
    for guest in guests:
        try:
            await bot.send_message(
                chat_id=guest.id,
                text=question['question'],
                reply_markup=ikb_guest_answer_menu(guest.id, callback_data.id, question['answers']),
            )
        except Exception as e:
            pass
    await callback.answer(
        text=f'Вопрос:\n{question['question']}\nОтправлен',
        show_alert=True,
    )


@opinions_router.callback_query(CallbackQuestion.filter(F.button == 'amount'))
async def get_answers_amount(callback: CallbackQuery, callback_data: CallbackQuestion, bot: Bot, state: FSMContext):
    data = await state.get_data()
    all_guests = await requests.all_guests()
    done_answers = await requests.get_users_answers(int(callback_data.id))
    question = data[callback_data.id]['question']
    await callback.answer(
        text=f'На вопрос:\n{question}\nОтветили {len(done_answers)}/{len(all_guests)}',
        show_alert=True,
    )


@opinions_router.callback_query(CallbackQuestion.filter(F.button == 'get_result'))
async def get_guests_answers_result(callback: CallbackQuery, callback_data: CallbackQuestion, bot: Bot,
                                    state: FSMContext):
    question = await requests.get_question(int(callback_data.id))
    answers = {str(answer.answer_id): {'answer': answer.answer, 'amount': 0} for answer in question.answers}
    for answer in question.guest_answer:
        answers[str(answer.answer_id)]['amount'] += 1
    await state.update_data(
        {'guests_answers': answers}
    )
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=f'{question.question}\nПоказать ответы:',
        reply_markup=ikb_guests_answers_admin_menu(callback_data.id, answers),
    )


@opinions_router.callback_query(CallbackQuestion.filter(F.button == 'reset'))
async def reset_guests_answers(callback: CallbackQuery, callback_data: CallbackQuestion, bot: Bot, state: FSMContext):
    data = await state.get_data()
    question = data[callback_data.id]['question']
    await requests.reset_users_answers(int(callback_data.id))
    await callback.answer(
        text=f'Ответы гостей на вопрос:\n{question}\nСброшены!',
        show_alert=True,
    )


@opinions_router.callback_query(CallbackQuestion.filter(F.button == 'delete_question'))
async def delete_question(callback: CallbackQuery, callback_data: CallbackQuestion, bot: Bot, state: FSMContext):
    data = await state.get_data()
    question = data[callback_data.id]['question']
    await requests.delete_question(int(callback_data.id))
    await callback.answer(
        text=f'Вопрос:\n{question}\nУдален!',
        show_alert=True,
    )
    await start_opinions(callback, state, bot)


@opinions_router.callback_query(CallbackPushAnswer.filter(F.button == 'push'))
async def show_guests_answers(callback: CallbackQuery, callback_data: CallbackPushAnswer, bot: Bot, state: FSMContext):
    question = await state.get_value(callback_data.question_id)
    answers = await state.get_value('guests_answers')
    answer = answers.pop(callback_data.answer_id)
    await state.update_data(
        {'guests_answers': answers}
    )

    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=f'{question['question']}\nПоказать ответы:',
        reply_markup=ikb_guests_answers_admin_menu(callback_data.question_id, answers)
    )


@opinions_router.callback_query(CallbackQuestion.filter(F.button == 'question'))
async def opinion_answer(callback: CallbackQuery, callback_data: CallbackQuestion, state: FSMContext, bot: Bot):
    data = await state.get_data()
    question = data[callback_data.id]['question']
    pusher_data = data['pusher_data']
    pusher_data['question'] = question
    await async_pusher.trigger(pusher_data)

    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=question,
        reply_markup=ikb_question_menu(callback_data.id),
    )
