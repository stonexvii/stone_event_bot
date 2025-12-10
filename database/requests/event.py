from datetime import date

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .connection import connection
from ..tables import Question, Event


@connection
async def new_event(description: str, event_date: date, session: AsyncSession):
    event = Event(description=description, date=event_date)
    session.add(event)
    await session.commit()


@connection
async def get_event(event_id: int, session: AsyncSession):
    event = await session.scalar(
        select(Event).options(selectinload(Event.questions).selectinload(Question.answers)).where(
            Event.id == event_id))
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
