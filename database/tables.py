from datetime import date

from sqlalchemy import String, BigInteger, Integer, ForeignKey, Date, Boolean, UniqueConstraint
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Event(Base):
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False, default='TITLE')
    description: Mapped[str] = mapped_column(String(100), nullable=True)
    date: Mapped[date] = mapped_column(Date)
    is_done: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    users = relationship('User', back_populates='event')
    questions = relationship('Question', back_populates='event', cascade='all, delete-orphan', passive_deletes=True)


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(900), nullable=True)
    username: Mapped[str] = mapped_column(String(100), nullable=True)
    event_id: Mapped[int] = mapped_column(ForeignKey('events.id'), nullable=False)
    event_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_sending: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    event = relationship('Event', back_populates='users')
    answers = relationship('UserAnswer', back_populates='user', cascade='all, delete-orphan', passive_deletes=True)


class Question(Base):
    __tablename__ = 'questions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey('events.id', ondelete="CASCADE"), nullable=False)
    question: Mapped[str] = mapped_column(String(900))

    event = relationship('Event', back_populates='questions', passive_deletes=True)
    answers = relationship('Answer', back_populates='question', cascade='all, delete-orphan', passive_deletes=True)
    users_answers = relationship('UserAnswer', back_populates='question', cascade='all, delete-orphan',
                                 passive_deletes=True)


class Answer(Base):
    __tablename__ = 'answers'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    question_id: Mapped[int] = mapped_column(ForeignKey('questions.id', ondelete="CASCADE"), nullable=False)
    answer_id: Mapped[int] = mapped_column(Integer)
    answer: Mapped[str] = mapped_column(String(100))
    question = relationship('Question', back_populates='answers')

    users_answers = relationship('UserAnswer', back_populates='answer', cascade='all, delete-orphan',
                                 passive_deletes=True)


class UserAnswer(Base):
    __tablename__ = 'users_answers'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey('questions.id', ondelete="CASCADE"), nullable=False)
    answer_id: Mapped[int] = mapped_column(Integer, ForeignKey('answers.id', ondelete="CASCADE"), nullable=False)

    user = relationship('User', back_populates='answers')
    question = relationship('Question', back_populates='users_answers')
    answer = relationship('Answer', back_populates='users_answers')

    __table_args__ = (
        UniqueConstraint('user_id', 'question_id', name='uq_user_question'),
    )
