from aiogram.filters.callback_data import CallbackData


class CallbackTopGame(CallbackData, prefix='CTG'):
    button: str
    id: int = 0


class CallbackQuestion(CallbackData, prefix='CQ'):
    button: str
    id: int


class CallbackGuestAnswer(CallbackData, prefix='CGA'):
    user_tg_id: int
    question_id: int = 0
    answer_id: int = 0
    answer_list_id: int = 0


class CallbackPushAnswer(CallbackData, prefix='CPA'):
    button: str
    question_id: int
    answer_id: int


class CallbackMenu(CallbackData, prefix='CM'):
    button: str


class CallbackEvent(CallbackData, prefix='CE'):
    button: str
    event_id: int


class CallbackBackButton(CallbackData, prefix='CB'):
    button: str
