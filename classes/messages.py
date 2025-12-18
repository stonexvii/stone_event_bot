import json


class PusherMessage:

    def __init__(self, answers_amount):
        self._title = 'HEADER'
        self._question = None
        for i in range(1, answers_amount + 1):
            self.__setattr__(f'{i}', None)

    @property
    def json(self):
        message = {
            'question': self._question if self._question else self._title,
        }
        for key, value in self.__dict__.items():
            if key not in {'_title', '_question'}:
                message[key] = value
        return json.dumps(message, ensure_ascii=False)

    def set_title(self, title: str):
        self._title = title

    def set_question(self, question: str):
        self._question = question

    def set_answer(self, answer: int | str, **kwargs):
        self.__setattr__(f'{answer}', kwargs)

    def reset(self):
        for key, value in self.__dict__.items():
            if key != '_title':
                self.__setattr__(key, None)
