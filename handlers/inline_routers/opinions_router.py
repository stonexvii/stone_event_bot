from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from classes import async_pusher, current_event
from classes.messages import PusherMessage
from database import requests
from fsm import Events
from keyboards import *
from keyboards.callback_data import CallbackMenu, CallbackBackButton, CallbackQuestion, \
    CallbackPushAnswer, CallbackEvent
from middleware import AdminMiddleware
from .menu import main_menu

opinions_router = Router()
opinions_router.callback_query.middleware(AdminMiddleware())


@opinions_router.callback_query(CallbackEvent.filter(F.button == 'target_event'))
@opinions_router.callback_query(CallbackMenu.filter(F.button == 'opinions_menu'))
async def start_opinions(callback: CallbackQuery, callback_data: CallbackEvent, bot: Bot):
    if isinstance(callback_data, CallbackEvent):
        await current_event.activate()
        async_pusher.set_message(PusherMessage(4))
        async_pusher.set_title(current_event.title)
    if not current_event.id:
        events = await requests.get_events()
        msg_text = 'Выберите мероприятие:'
        keyboard = ikb_select_event(events)
    else:
        await async_pusher.set_message(PusherMessage(4))
        msg_text = 'Выбери вопрос:'
        keyboard = ikb_opinions_menu(current_event.questions)
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=msg_text,
        reply_markup=keyboard,
    )


@opinions_router.callback_query(CallbackBackButton.filter())
async def back_to_main_menu(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await main_menu(callback, bot, state)


@opinions_router.callback_query(CallbackQuestion.filter(F.button == 'question'))
async def select_question(callback: CallbackQuery, callback_data: CallbackQuestion, bot: Bot):
    question = current_event.get_question(callback_data.id)
    # async_pusher.set_message(PusherMessageOpinions())
    await async_pusher.set_question(question.question)
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=question.question + '\n\n' + '\n'.join([f' - {answer.answer}' for answer in question.answers]),
        reply_markup=ikb_question_menu(question.id),
    )


@opinions_router.callback_query(CallbackMenu.filter(F.button == 'new_event'))
async def new_event(callback: CallbackQuery, bot: Bot, state: FSMContext):
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
    await requests.delete_questions(current_event.id)
    await callback.answer(
        text='Все вопросы удалены!',
        show_alert=True,
    )


@opinions_router.callback_query(CallbackQuestion.filter(F.button == 'send_question'))
async def send_question(callback: CallbackQuery, callback_data: CallbackQuestion, bot: Bot):
    users = await requests.get_event_users(current_event.id)
    question = current_event.get_question(callback_data.id)
    success, failed = 0, 0
    for user in users:
        try:
            await bot.send_message(
                chat_id=user.id,
                text=question.question,
                reply_markup=ikb_guest_answer_menu(user.id, question),
            )
            success += 1
        except Exception as e:
            failed += 1
    await callback.answer(
        text=f'Вопрос:\n{question.question}\nОтправлен!\nУспешно: {success}\nОшибка: {failed}',
        show_alert=True,
    )


@opinions_router.callback_query(CallbackQuestion.filter(F.button == 'amount'))
async def get_answers_amount(callback: CallbackQuery, callback_data: CallbackQuestion):
    all_guests = await requests.get_event_users(current_event.id)
    done_answers = await requests.get_users_answers(callback_data.id)
    question = current_event.get_question(callback_data.id)
    await callback.answer(
        text=f'На вопрос:\n{question.question}\nОтветили {len(done_answers)}/{len(all_guests)}',
        show_alert=True,
    )


@opinions_router.callback_query(CallbackQuestion.filter(F.button == 'get_result'))
async def get_users_answers_result(callback: CallbackQuery, callback_data: CallbackQuestion, bot: Bot,
                                   state: FSMContext):
    question = await requests.get_question(callback_data.id)
    answers = {str(answer.answer_id): {'text': answer.answer, 'amount': 0} for answer in question.answers}
    for answer in question.users_answers:
        answers[str(answer.answer_id)]['amount'] += 1
    answers = {idx: answer for idx, answer in
               enumerate(sorted(answers.values(), key=lambda x: x['amount'], reverse=True), 1)}
    await state.update_data(
        {'users_answers': answers}
    )
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=f'{question.question}\nПоказать ответы:',
        reply_markup=ikb_guests_answers_admin_menu(callback_data.id, answers),
    )


@opinions_router.callback_query(CallbackQuestion.filter(F.button == 'reset'))
async def reset_guests_answers(callback: CallbackQuery, callback_data: CallbackQuestion, bot: Bot, state: FSMContext):
    question = current_event.get_question(callback_data.id)
    await requests.reset_users_answers(callback_data.id)
    await callback.answer(
        text=f'Ответы гостей на вопрос:\n{question}\nСброшены!',
        show_alert=True,
    )


@opinions_router.callback_query(CallbackQuestion.filter(F.button == 'delete_question'))
async def delete_question(callback: CallbackQuery, callback_data: CallbackQuestion, bot: Bot, state: FSMContext):
    question = current_event.get_question(callback_data.id)
    await requests.delete_question(callback_data.id)
    await callback.answer(
        text=f'Вопрос:\n{question}\nУдален!',
        show_alert=True,
    )
    await start_opinions(callback, state, bot)


@opinions_router.callback_query(CallbackPushAnswer.filter(F.button == 'push'))
async def show_guests_answers(callback: CallbackQuery, callback_data: CallbackPushAnswer, bot: Bot, state: FSMContext):
    question = current_event.get_question(callback_data.question_id)
    answers = await state.get_value('users_answers')
    answer = answers.pop(callback_data.answer_id)
    await async_pusher.set_answer(callback_data.answer_id, **answer)
    print(answer)
    await state.update_data(
        {'users_answers': answers}
    )
    await bot.edit_message_text(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        text=f'{question.question}\nПоказать ответы:',
        reply_markup=ikb_guests_answers_admin_menu(callback_data.question_id, answers)
    )
