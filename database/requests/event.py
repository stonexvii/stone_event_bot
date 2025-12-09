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
async def get_event(event_id: int, session: AsyncSession):
    event = await session.scalar(select(Event).where(Event.id == event_id))
    return event


@connection
async def get_events(session: AsyncSession):
    events = await session.scalars(select(Event).where(Event.is_done.is_(False)))
    return events.all()


@connection
async def activate_event(event_id: int, session: AsyncSession):
    await session.execute(update(Event).values(active=False))
    await session.execute(update(Event).where(Event.id == event_id).values(active=True))
    await session.commit()


@connection
async def title_event(event_id: int, title: str, session: AsyncSession):
    await session.execute(update(Event).where(Event.id == event_id).values(title=title))
    await session.commit()


@connection
async def done_event(event_id: int, session: AsyncSession):
    await session.execute(update(Event).where(Event.id == event_id).values(is_done=True))
    await session.commit()
