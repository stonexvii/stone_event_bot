from aiogram.fsm.state import State, StatesGroup


class TopGame(StatesGroup):
    wait_for_request = State()
    show_answers = State()


class Events(StatesGroup):
    new_event = State()
    set_title = State()


class UserName(StatesGroup):
    wait_for_answer = State()


class QuestionForUser(StatesGroup):
    question_for_user = State()
    wait_user_answer = State()
