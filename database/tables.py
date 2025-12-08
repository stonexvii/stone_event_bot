from datetime import date

from sqlalchemy import String, BigInteger, Integer, ForeignKey, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(100), nullable=True)
    register_date: Mapped[date] = mapped_column(Date)
    is_guest: Mapped[bool] = mapped_column(Boolean, default=True)


class Question(Base):
    __tablename__ = 'questions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question: Mapped[str] = mapped_column(String(900))
    answers = relationship('Answer', back_populates='question', cascade='all, delete-orphan',
                           passive_deletes=True)
    user_answer = relationship('UserAnswer', back_populates='question', cascade='all, delete-orphan',
                               passive_deletes=True)


class Answer(Base):
    __tablename__ = 'answers'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    question_id: Mapped[int] = mapped_column(ForeignKey('questions.id', ondelete="CASCADE"), nullable=False)
    answer_id: Mapped[int] = mapped_column(Integer)
    answer: Mapped[str] = mapped_column(String(100))
    question = relationship('Question', back_populates='answers')


class UserAnswer(Base):
    __tablename__ = 'users_answers'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    question_id: Mapped[str] = mapped_column(Integer, ForeignKey('questions.id', ondelete="CASCADE"), nullable=False)
    answer_id: Mapped[int] = mapped_column(Integer)
    question = relationship('Question', back_populates='user_answer')
