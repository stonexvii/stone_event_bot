from aiogram.filters.callback_data import CallbackData


class CallbackTopGame(CallbackData, prefix='CTG'):
    button: str
    id: int = 0


class CallbackQuestion(CallbackData, prefix='CQ'):
    button: str
    id: str


class CallbackGuestAnswer(CallbackData, prefix='CGA'):
    user_tg_id: int
    question_id: str
    answer_id: str


class CallbackPushAnswer(CallbackData, prefix='CPA'):
    button: str
    question_id: str
    answer_id: int


class CallbackMenu(CallbackData, prefix='CM'):
    button: str


class CallbackBackButton(CallbackData, prefix='CB'):
    button: str
