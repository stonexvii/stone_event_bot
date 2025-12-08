from .connection import connection

from aiogram.types import Message

from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import selectinload

from ..tables import Base, Answer, Question, User, GuestAnswer, Guest, Event
from datetime import date


@connection
async def new_question(question: str, answers: list[str], session: AsyncSession):
    question = Question(question=question)
    session.add(question)
    await session.commit()
    await session.refresh(question)
    data = [Answer(question_id=question.id, answer_id=idx, answer=answer) for idx, answer in enumerate(answers, 1)]
    session.add_all(data)
    await session.commit()


@connection
async def get_question(question_id: int, session: AsyncSession) -> Question:
    question = await session.scalar(
        select(Question).options(selectinload(Question.answers), selectinload(Question.guest_answer)).where(
            Question.id == question_id))
    return question


@connection
async def get_answer(question_id: int, answer_id: int, session: AsyncSession) -> Answer:
    answer = await session.scalar(
        select(Answer).where(Answer.question_id == question_id, Answer.answer_id == answer_id))
    return answer


@connection
async def all_questions(session: AsyncSession):
    questions = await session.scalars(select(Question).options(selectinload(Question.answers)))
    return questions.all()


@connection
async def delete_question(question_id: int, session: AsyncSession):
    question = await session.scalar(select(Question).where(Question.id == question_id))
    await session.delete(question)
    await session.commit()


@connection
async def delete_questions(session: AsyncSession):
    questions = await all_questions()
    for question in questions:
        await session.delete(question)
    await session.commit()
