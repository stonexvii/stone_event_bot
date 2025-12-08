# from datetime import date
# from datetime import datetime
# from asyncio import sleep
# from aiogram import Router, Bot, F
# from aiogram.fsm.context import FSMContext
# from aiogram.types import CallbackQuery, Message
#
# from ai_gpt import GPTMessage
# from ai_gpt.enums import GPTRole
# # from data import get_examples
# # from database import requests
# # from database.tables import User
# from fsm import Generate, Reminder, TopGame, Events
# from keyboards import *
# # from keyboards.callback_data import CallbackBackButton, CallbackMainMenu, CallbackApprove
# # from scheduler.scheduler import schedule_event
# from utils import FileManager
# from utils.enums import Path
# from utils.bot import db_to_dict
# from keyboards.callback_data import CallbackTopGame, CallbackMenu, CallbackBackButton, CallbackQuestion, \
#     CallbackPushAnswer
# from middleware import AdminMiddleware
# from database import requests
# from pusher_app import async_pusher, push_message
#
# callback_router = Router()
# callback_router.callback_query.middleware(AdminMiddleware())
#
#
# async def main_menu(callback: CallbackQuery, bot: Bot, state: FSMContext):
#     await state.clear()
#     await bot.edit_message_text(
#         chat_id=callback.from_user.id,
#         message_id=callback.message.message_id,
#         text='Работаю',
#         reply_markup=ikb_main_menu(),
#     )
#
#
# async def admin_events_menu(update: Message | CallbackQuery, bot: Bot, state: FSMContext):
#     data = await state.get_data()
#     await state.clear()
#     events = await requests.get_events()
#     if events:
#         msg_text = '\n'.join([f'{line.id}. ({line.date}) {line.description}' for line in events])
#     else:
#         msg_text = 'У тебя нет мероприятий'
#     message_id = data['message_id'] if isinstance(update, Message) else update.message.message_id
#     await bot.edit_message_text(
#         chat_id=update.from_user.id,
#         message_id=message_id,
#         text=msg_text,
#         reply_markup=ikb_events_menu(),
#     )
#
#
# @callback_router.callback_query(CallbackBackButton.filter())
# async def back_to_main_menu(callback: CallbackQuery, bot: Bot, state: FSMContext):
#     await main_menu(callback, bot, state)
#
#
# @callback_router.callback_query(CallbackMenu.filter(F.button == 'events'))
# async def admin_events(callback: CallbackQuery, bot: Bot, state: FSMContext):
#     await state.clear()
#     await admin_events_menu(callback, bot, state)
#
#
# @callback_router.callback_query(CallbackMenu.filter(F.button == 'new_event'))
# async def new_event(callback: CallbackQuery, callback_data: CallbackMenu, bot: Bot, state: FSMContext):
#     await state.set_state(Events.new_event)
#     await state.update_data({'message_id': callback.message.message_id})
#     await bot.edit_message_text(
#         chat_id=callback.from_user.id,
#         message_id=callback.message.message_id,
#         text='Введите: Описание мероприятия YYYY/MM/DD',
#         reply_markup=ikb_cancel_new_event(),
#     )
#
#
# @callback_router.callback_query(CallbackMenu.filter(F.button == 'top'))
# async def start_top_game(callback: CallbackQuery, callback_data: CallbackMenu, bot: Bot, state: FSMContext):
#     await state.set_state(TopGame.wait_for_request)
#     await bot.edit_message_text(
#         chat_id=callback.from_user.id,
#         message_id=callback.message.message_id,
#         text='Задавай тему для игры',
#         reply_markup=ikb_back_button(),
#
#     )
#
#
# @callback_router.callback_query(CallbackTopGame.filter(), TopGame.show_answers)
# async def top_game_answer(callback: CallbackQuery, callback_data: CallbackTopGame, state: FSMContext, bot: Bot):
#     # msg_text = await FileManager.read(Path.START_COMMAND.value, user_name=user.name)
#     await callback.answer(
#         text='',
#     )
#     message_data = await state.get_data()
#     message_data[callback_data.button]['visible'] = True
#     await state.update_data(
#         **message_data,
#     )
#     await bot.edit_message_text(
#         chat_id=callback.from_user.id,
#         message_id=callback.message.message_id,
#         text=message_data['question'],
#         reply_markup=ikb_top_game_answers(message_data),
#     )
#
#
# @callback_router.callback_query(CallbackMenu.filter(F.button == 'opinions'))
# async def start_opinions(callback: CallbackQuery, state: FSMContext, bot: Bot):
#     questions = await requests.all_questions()
#     questions = db_to_dict(questions)
#     pusher_data = {
#         'question': 'Светлана и Василий',
#         'answer_1': '',
#         'answer_2': '',
#         'answer_3': '',
#         'answer_4': '',
#     }
#     await async_pusher.trigger(pusher_data)
#     await state.update_data(**questions, pusher_data=pusher_data)
#     await bot.edit_message_text(
#         chat_id=callback.from_user.id,
#         message_id=callback.message.message_id,
#         text='Вопросы',
#         reply_markup=ikb_opinions_menu(questions),
#     )
#
#
# @callback_router.callback_query(CallbackQuestion.filter(F.button == 'send_question'))
# async def send_question(callback: CallbackQuery, callback_data: CallbackQuestion, bot: Bot, state: FSMContext):
#     data = await state.get_data()
#     guests = await requests.all_guests()
#     question = data[callback_data.id]
#     for guest in guests:
#         try:
#             await bot.send_message(
#                 chat_id=guest.id,
#                 text=question['question'],
#                 reply_markup=ikb_guest_answer_menu(guest.id, callback_data.id, question['answers']),
#             )
#         except Exception as e:
#             pass
#     await callback.answer(
#         text=f'Вопрос:\n{question['question']}\nОтправлен',
#         show_alert=True,
#     )
#
#
# @callback_router.callback_query(CallbackQuestion.filter(F.button == 'amount'))
# async def get_answers_amount(callback: CallbackQuery, callback_data: CallbackQuestion, bot: Bot, state: FSMContext):
#     data = await state.get_data()
#     all_guests = await requests.all_guests()
#     done_answers = await requests.get_users_answers(int(callback_data.id))
#     question = data[callback_data.id]['question']
#     await callback.answer(
#         text=f'На вопрос:\n{question}\nОтветили {len(done_answers)}/{len(all_guests)}',
#         show_alert=True,
#     )
#
#
# @callback_router.callback_query(CallbackQuestion.filter(F.button == 'get_result'))
# async def get_guests_answers_result(callback: CallbackQuery, callback_data: CallbackQuestion, bot: Bot,
#                                     state: FSMContext):
#     question = await requests.get_question(int(callback_data.id))
#     # print(question.guest_answer)
#     # guests_answers = await requests.get_users_answers(int(callback_data.id))
#     answers = {str(answer.answer_id): {'answer': answer.answer, 'amount': 0} for answer in question.answers}
#     for answer in question.guest_answer:
#         answers[str(answer.answer_id)]['amount'] += 1
#     await state.update_data(
#         {'guests_answers': answers}
#     )
#     await bot.edit_message_text(
#         chat_id=callback.from_user.id,
#         message_id=callback.message.message_id,
#         text=f'{question.question}\nПоказать ответы:',
#         reply_markup=ikb_guests_answers_admin_menu(callback_data.id, answers),
#     )
#     # data = await state.get_data()
#     # guests = await requests.all_guests()
#     # question = data[callback_data.id]
#     # for guest in guests:
#     #     try:
#     #         await bot.send_message(
#     #             chat_id=guest.id,
#     #             text=question['question'],
#     #             reply_markup=ikb_guest_answer_menu(guest.id, callback_data.id, question['answers']),
#     #         )
#     #     except Exception as e:
#     #         pass
#     # await callback.answer(
#     #     text=f'Вопрос:\n{question['question']}\nОтправлен',
#     #     show_alert=True,
#     # )
#
#
# @callback_router.callback_query(CallbackPushAnswer.filter(F.button == 'push'))
# async def show_guests_answers(callback: CallbackQuery, callback_data: CallbackPushAnswer, bot: Bot, state: FSMContext):
#     question = await state.get_value(callback_data.question_id)
#     answers = await state.get_value('guests_answers')
#     answer = answers.pop(callback_data.answer_id)
#     await state.update_data(
#         {'guests_answers': answers}
#     )
#
#     await bot.edit_message_text(
#         chat_id=callback.from_user.id,
#         message_id=callback.message.message_id,
#         text=f'{question['question']}\nПоказать ответы:',
#         reply_markup=ikb_guests_answers_admin_menu(callback_data.question_id, answers)
#     )
#
#
# @callback_router.callback_query(CallbackQuestion.filter(F.button == 'reset'))
# async def reset_guests_answers(callback: CallbackQuery, callback_data: CallbackQuestion, bot: Bot, state: FSMContext):
#     data = await state.get_data()
#     question = data[callback_data.id]['question']
#     await requests.reset_users_answers(int(callback_data.id))
#     await callback.answer(
#         text=f'Ответы гостей на вопрос:\n{question}\nСброшены!',
#         show_alert=True,
#     )
#
#
# @callback_router.callback_query(CallbackQuestion.filter(F.button == 'delete_question'))
# async def delete_question(callback: CallbackQuery, callback_data: CallbackQuestion, bot: Bot, state: FSMContext):
#     data = await state.get_data()
#     question = data[callback_data.id]['question']
#     await requests.delete_question(int(callback_data.id))
#     await callback.answer(
#         text=f'Вопрос:\n{question}\nУдален!',
#         show_alert=True,
#     )
#     await start_opinions(callback, state, bot)
#
#
# @callback_router.callback_query(CallbackQuestion.filter(F.button == 'question'))
# async def opinion_answer(callback: CallbackQuery, callback_data: CallbackQuestion, state: FSMContext, bot: Bot):
#     # questions = await requests.all_questions()
#     # await bot.edit_message_text(
#     #     chat_id=callback.from_user.id,
#     #     message_id=callback.message.message_id,
#     #     text='Вопросы',
#     #     reply_markup=ikb_opinions_menu(questions),
#     # )
#     data = await state.get_data()
#     question = data[callback_data.id]['question']
#     pusher_data = data['pusher_data']
#     pusher_data['question'] = question
#     await async_pusher.trigger(pusher_data)
#     # await callback.answer(
#     #     text=str(data[callback_data.id]),
#     # )
#     await bot.edit_message_text(
#         chat_id=callback.from_user.id,
#         message_id=callback.message.message_id,
#         text=question,
#         reply_markup=ikb_question_menu(callback_data.id),
#     )
#     # msg_text = await FileManager.read(Path.START_COMMAND.value, user_name=user.name)
#     # await bot.edit_message_text(
#     #     chat_id=callback.from_user.id,
#     #     message_id=callback.message.message_id,
#     #     text=msg_text,
#     #     reply_markup=ikb_main_menu(),
#     # )
#
#
# @callback_router.callback_query(CallbackMenu.filter(F.button == 'delete_all'))
# async def delete_all_questions(callback: CallbackQuery, bot: Bot, state: FSMContext):
#     await requests.delete_questions()
#     await callback.answer(
#         text='Все вопросы удалены!',
#         show_alert=True,
#     )
# #
# #
# # @callback_router.callback_query(CallbackMainMenu.filter(F.button == 'apply'))
# # async def apply_welcome(callback: CallbackQuery, state: FSMContext, bot: Bot):
# #     msg_text = await FileManager.read(Path.MESSAGE.value, 'welcome_name', user_name=callback.from_user.full_name)
# #     await requests.new_user(
# #         user_tg_id=callback.from_user.id,
# #         name=callback.from_user.full_name,
# #         tg_username=callback.from_user.username,
# #     )
# #     await bot.edit_message_text(
# #         chat_id=callback.from_user.id,
# #         message_id=callback.message.message_id,
# #         text=msg_text,
# #         reply_markup=ikb_welcome('Пропустить', 'skip'),
# #     )
# #     await state.set_state(UserName.wait_for_answer)
# #     await state.update_data(
# #         {
# #             'message_id': callback.message.message_id,
# #         }
# #     )
# #
# #
# # @callback_router.callback_query(CallbackMainMenu.filter(F.button == 'skip'))
# # async def skip_name(callback: CallbackQuery, user: User, state: FSMContext, bot: Bot):
# #     await callback_main_menu(callback, user, state, bot)
# #
# #
# # @callback_router.callback_query(CallbackMainMenu.filter())
# # async def menu_item(callback: CallbackQuery, callback_data: CallbackMainMenu, user: User, state: FSMContext, bot: Bot):
# #     examples = await get_examples(callback_data.button)
# #     msg_text = await FileManager.read(Path.MESSAGE.value, f'start_{callback_data.button}', user_name=user.name,
# #                                       examples=examples)
# #     await bot.edit_message_text(
# #         chat_id=callback.from_user.id,
# #         message_id=callback.message.message_id,
# #         text=msg_text,
# #         reply_markup=ikb_back_button(),
# #     )
# #     state_name = Generate
# #     if callback_data.button == 'reminder':
# #         state_name = Reminder
# #     await state.set_state(state_name.wait_for_answer)
# #     msg_list = GPTMessage(callback_data.button)
# #     add_task = ''
# #     if idx := callback_data.id:
# #         task = await requests.get_task(idx)
# #         add_task = f'\nПоздравь {task.name} с {task.event_type}'
# #     msg_list.update(GPTRole.USER, f'Привет, меня зовут {user.name}!' + add_task)
# #     await state.update_data({'messages': msg_list.json()})
# #
# #
# # @callback_router.callback_query(CallbackBackButton.filter(F.button == 'to_main'))
# # async def back_to_main_menu(callback: CallbackQuery, user: User, state: FSMContext, bot: Bot):
# #     await callback_main_menu(callback, user, state, bot)
# #
# #
# # @callback_router.callback_query(CallbackApprove.filter())
# # async def approve_callback(callback: CallbackQuery, callback_data: CallbackApprove, user: User, state: FSMContext,
# #                            bot: Bot):
# #     if callback_data.button == 'generate':
# #         msg_text = 'Супер!\nИстория нашей переписки очищена'
# #         await bot.send_message(
# #             chat_id=callback.from_user.id,
# #             text=callback.message.text.split('\n\n', 1)[1].rsplit('\n\n', 1)[0],
# #         )
# #     else:
# #         msg_text = 'Отлично!\nЯ записал уведомление и оповещу тебя как и договорились!'
# #         json_data = await state.get_value('json')
# #         reminder = datetime.fromisoformat(json_data['reminder'])
# #         event_date = date.fromisoformat(json_data['date'])
# #         task = await requests.new_task(
# #             user_tg_id=callback.from_user.id,
# #             user_name=user.name,
# #             event_type=json_data['event'],
# #             event_date=event_date,
# #             reminder=reminder,
# #         )
# #         data = {
# #             'task_id': task.id,
# #             'user_name': user.name,
# #             'name': json_data['name'],
# #             'event': json_data['event'],
# #             'date': event_date,
# #             'reminder': reminder,
# #         }
# #         schedule_event(callback.from_user.id, data, bot)
# #     await callback.answer(
# #         text=msg_text,
# #         show_alert=True,
# #     )
# #     await sleep(3)
# #     await new_main_menu(callback, user, state, bot)
