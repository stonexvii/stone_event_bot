# from aiogram.types import Message
#
# from sqlalchemy import select, insert, update
# from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
# from sqlalchemy.orm import selectinload
#
# import config
# from .db_engine import async_session, engine
# from .tables import Base, Answer, Question, User, UserAnswer, Guest, Event
# from datetime import date
#
#
# def connection(function):
#     async def wrapper(*args, **kwargs):
#         async with async_session() as session:
#             try:
#                 return await function(*args, session=session, **kwargs)
#             except Exception as e:
#                 await session.rollback()
#                 raise e
#             finally:
#                 await session.close()
#
#     return wrapper
#
#
# async def create_tables():
#     async with engine.begin() as connect:
#         await connect.run_sync(Base.metadata.create_all)
#
#
# @connection
# async def new_event(description: str, event_date: date, session: AsyncSession):
#     event = Event(description=description, date=event_date)
#     session.add(event)
#     await session.commit()
#
#
# @connection
# async def get_events(session: AsyncSession):
#     events = await session.scalars(select(Event))
#     return events.all()
#
#
# @connection
# async def new_user(tg_user_id: int, tg_username: str, event_id: int, session: AsyncSession):
#     user = User(id=tg_user_id, username=tg_username, event_id=int)
#     guest = Guest(id=tg_user_id)
#     session.add_all([user, guest])
#     await session.commit()
#
#
# @connection
# async def new_question(question: str, answers: list[str], session: AsyncSession):
#     question = Question(question=question)
#     session.add(question)
#     await session.commit()
#     await session.refresh(question)
#     data = [Answer(question_id=question.id, answer_id=idx, answer=answer) for idx, answer in enumerate(answers, 1)]
#     session.add_all(data)
#     await session.commit()
#
#
# @connection
# async def all_questions(session: AsyncSession):
#     questions = await session.scalars(select(Question).options(selectinload(Question.answers)))
#     return questions.all()
#
#
# @connection
# async def delete_questions(session: AsyncSession):
#     questions = await all_questions()
#     for question in questions:
#         await session.delete(question)
#     await session.commit()
#
# #
# #
# # @connection
# # async def set_question(question_id: int, question_text: str, answers: list[str], session: AsyncSession):
# #     question = await session.scalar(select(QuestionsTable).where(QuestionsTable.id == question_id))
# #     if question:
# #         await delete_question(question_id)
# #     question = QuestionsTable(id=question_id, question=question_text)
# #     session.add(question)
# #     await session.commit()
# #     answers = [AnswersTable(question_id=question_id, answer_id=answer_id, answer=answer) for answer_id, answer in
# #                enumerate(answers, 1)]
# #     session.add_all(answers)
# #     await session.commit()
# #
# #
# # @connection
# # async def delete_question(question_id: int, session: AsyncSession):
# #     question = await session.scalar(select(QuestionsTable).where(QuestionsTable.id == question_id))
# #     if question:
# #         await session.delete(question)
# #         await session.commit()
# #
# #
# # @connection
# # async def get_question(question_id: int, session: AsyncSession):
# #     question = await session.scalar(select(QuestionsTable).where(QuestionsTable.id == question_id))
# #     if question:
# #         answers = await session.scalars(
# #             select(AnswersTable).where(AnswersTable.question_id == question_id))
# #         return question, answers.all()
# #
# #
# # @connection
# # async def add_user_answer(user_id: int, question_id: int, answer_id: int, session: AsyncSession):
# #     session.add(UserAnswers(
# #         user_id=user_id,
# #         question_id=question_id,
# #         answer_id=answer_id,
# #     ))
# #     await session.commit()
# #
# #
# # @connection
# # async def collect_answers(question_id: int, session: AsyncSession):
# #     response = await session.scalars(select(UserAnswers.answer_id).where(UserAnswers.question_id == question_id))
# #     return response.all()
# #
# #
# # @connection
# # async def all_users(session: AsyncSession):
# #     response = await session.scalars(select(Users.id))
# #     return response.all()
# #
# #
# # @connection
# # async def all_questions(session: AsyncSession):
# #     response = await session.scalars(select(QuestionsTable))
# #     return response.all()
# #
# #
# # @connection
# # async def delete_answers(question_id: int, session: AsyncSession):
# #     answers = await session.scalars(select(UserAnswers).where(UserAnswers.question_id == question_id))
# #     for answer in answers.all():
# #         await session.delete(answer)
# #     await session.commit()
# #
# #
# # @connection
# # async def set_target_answer(question_id: int, answer_id: int, answer: str, session: AsyncSession):
# #     stmt = update(AnswersTable).where(AnswersTable.question_id == question_id,
# #                                       AnswersTable.answer_id == answer_id).values(answer=answer)
# #     await session.execute(stmt)
# #     await session.commit()
