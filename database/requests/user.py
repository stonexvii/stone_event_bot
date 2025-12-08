from .connection import connection

from aiogram.types import Message

from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ..tables import Base, Answer, Question, User, GuestAnswer, Guest, Event
from datetime import date


@connection
async def new_user(tg_user_id: int, tg_username: str, event_id: int, session: AsyncSession):
    user = User(id=tg_user_id, username=tg_username, event_id=event_id)
    guest = Guest(id=tg_user_id)
    session.add_all([user, guest])
    await session.commit()



