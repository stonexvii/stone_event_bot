from aiogram.filters.callback_data import CallbackData


class CallbackTopGame(CallbackData, prefix='CTG'):
    button: str
    id: int = 0


class CallbackQuestion(CallbackData, prefix='CQ'):
    button: str
    id: int


class CallbackMenu(CallbackData, prefix='CM'):
    button: str


class CallbackBackButton(CallbackData, prefix='CB'):
    button: str
