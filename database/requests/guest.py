from .connection import connection

from aiogram.types import Message

from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import selectinload

from ..tables import Base, Answer, Question, User, GuestAnswer, Guest, Event
from datetime import date


@connection
async def all_guests(session: AsyncSession):
    response = await session.scalars(select(Guest))
    return response.all()


@connection
async def add_guest_answer(tg_user_id: int, question_id: int, answer_id: int, session: AsyncSession):
    guest_answer = GuestAnswer(guest_id=tg_user_id, question_id=question_id, answer_id=answer_id)
    session.add(guest_answer)
    await session.commit()


@connection
async def get_users_answers(question_id: int, session: AsyncSession):
    guests_answers = await session.scalars(select(GuestAnswer).where(GuestAnswer.question_id == question_id))
    return guests_answers.all()


@connection
async def reset_users_answers(question_id: int, session: AsyncSession):
    guests_answers = await session.scalars(select(GuestAnswer).where(GuestAnswer.question_id == question_id))
    for guest_answer in guests_answers.all():
        await session.delete(guest_answer)
    await session.commit()
