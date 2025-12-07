from aiogram.fsm.state import State, StatesGroup


class TopGame(StatesGroup):
    wait_for_request = State()
    show_answers = State()


class UserName(StatesGroup):
    wait_for_answer = State()


class Generate(StatesGroup):
    wait_for_answer = State()


class Reminder(StatesGroup):
    wait_for_answer = State()
