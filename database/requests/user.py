from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .connection import connection
from ..tables import User, UserAnswer


@connection
async def new_user(tg_user_id: int, tg_username: str, event_id: int, session: AsyncSession):
    user = await session.scalar(select(User).where(User.id == tg_user_id))
    if user:
        return True
    user = User(id=tg_user_id, username=tg_username, event_id=event_id)
    session.add(user)
    await session.commit()
    await session.refresh(user)


@connection
async def get_event_users(event_id: int, session: AsyncSession):
    response = await session.scalars(select(User).where(User.event_id == event_id))
    return response.all()


@connection
async def add_user_answer(tg_user_id: int, question_id: int, answer_id: int, session: AsyncSession):
    answer = await session.scalar(
        select(UserAnswer).where(UserAnswer.user_id == tg_user_id, UserAnswer.question_id == question_id))
    if answer:
        answer.answer_id = answer_id
    else:
        new_answer = UserAnswer(
            user_id=tg_user_id,
            question_id=question_id,
            answer_id=answer_id,
        )
        session.add(new_answer)
    await session.commit()


@connection
async def get_users_answers(question_id: int, session: AsyncSession):
    guests_answers = await session.scalars(select(UserAnswer).where(UserAnswer.question_id == question_id))
    return guests_answers.all()


@connection
async def set_user_sending(user_tg_id: int, session: AsyncSession):
    await session.execute(update(User).where(User.id == user_tg_id).values(is_sending=True))
    await session.commit()


@connection
async def reset_users_answers(question_id: int, session: AsyncSession):
    guests_answers = await session.scalars(select(UserAnswer).where(UserAnswer.question_id == question_id))
    for guest_answer in guests_answers.all():
        await session.delete(guest_answer)
    await session.commit()
