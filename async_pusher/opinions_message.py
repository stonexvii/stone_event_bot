class PusherMessage:

    def __init__(self):
        self._header = 'HEADER'
        self._question = ''
        self._answer_1 = ''
        self._answer_2 = ''
        self._answer_3 = ''
        self._answer_4 = ''

    @property
    def json(self):
        message = {
            'question': self._question if self._question else self._header,
            'answer_1': self._answer_1,
            'answer_2': self._answer_2,
            'answer_3': self._answer_3,
            'answer_4': self._answer_4,
        }
        return message

    def set_answer(self, answer: int, message: str):
        self.__setattr__(f'_answer_{answer}', message)

    def set_question(self, question: str):
        self._question = question

    def reset(self):
        self._question = ''
        self._answer_1 = ''
        self._answer_2 = ''
        self._answer_3 = ''
        self._answer_4 = ''
