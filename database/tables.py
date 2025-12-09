from datetime import date

from sqlalchemy import String, BigInteger, Integer, ForeignKey, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Event(Base):
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    description: Mapped[str] = mapped_column(String(100), nullable=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False, default='TITLE')
    date: Mapped[date] = mapped_column(Date)

    users = relationship('User', back_populates='event', cascade='all, delete-orphan', passive_deletes=True)


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(900), nullable=True)
    username: Mapped[str] = mapped_column(String(100), nullable=True)
    event_id: Mapped[int] = mapped_column(ForeignKey('events.id', ondelete="CASCADE"), nullable=False)
    is_sending: Mapped[bool] = mapped_column(Boolean, default=False)

    event = relationship('Event', back_populates='users')


class Guest(Base):
    __tablename__ = 'guests'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    answers = relationship('GuestAnswer', back_populates='guest', cascade='all, delete-orphan', passive_deletes=True)


class Question(Base):
    __tablename__ = 'questions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question: Mapped[str] = mapped_column(String(900))

    answers = relationship('Answer', back_populates='question', cascade='all, delete-orphan', passive_deletes=True)
    guest_answer = relationship('GuestAnswer', back_populates='question', cascade='all, delete-orphan',
                                passive_deletes=True)


class Answer(Base):
    __tablename__ = 'answers'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    question_id: Mapped[int] = mapped_column(ForeignKey('questions.id', ondelete="CASCADE"), nullable=False)
    answer_id: Mapped[int] = mapped_column(Integer)
    answer: Mapped[str] = mapped_column(String(100))
    question = relationship('Question', back_populates='answers')

    guests_answers = relationship('GuestAnswer', back_populates='answer', cascade='all, delete-orphan',
                                  passive_deletes=True)


class GuestAnswer(Base):
    __tablename__ = 'guests_answers'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    guest_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('guests.id', ondelete="CASCADE"), nullable=False)
    question_id: Mapped[str] = mapped_column(Integer, ForeignKey('questions.id', ondelete="CASCADE"), nullable=False)
    answer_id: Mapped[int] = mapped_column(Integer, ForeignKey('answers.id', ondelete="CASCADE"), nullable=False)

    guest = relationship('Guest', back_populates='answers')
    question = relationship('Question', back_populates='guest_answer')
    answer = relationship('Answer', back_populates='guests_answers')
