from .connection import connection

from aiogram.types import Message

from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ..tables import Base, Answer, Question, User, GuestAnswer, Guest, Event
from datetime import date


@connection
async def new_event(description: str, event_date: date, session: AsyncSession):
    event = Event(description=description, date=event_date)
    session.add(event)
    await session.commit()


@connection
async def get_events(session: AsyncSession):
    events = await session.scalars(select(Event))
    return events.all()