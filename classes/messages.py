import json


# class Answer:
#
#     @property
#     def as_kwargs(self):
#         return self.__dict__
#
#
# class AnswerOpinion(Answer):
#
#     def __init__(self, text: str = '', amount: int = 0):
#         self.text = text
#         self.amount = amount
#
#
# class AnswerTop5(Answer):
#
#     def __init__(self, text: str = '', visible: bool = False):
#         self.text = text
#         self.visible = visible


class PusherMessage:

    def __init__(self, answers_amount):
        self._title = 'HEADER'
        self._question = None
        for i in range(1, answers_amount+1):
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

    def set_answer(self, answer: int, **kwargs):
        self.__setattr__(f'{answer}', kwargs)

    def reset(self):
        for key, value in self.__dict__.items():
            if key != '_title':
                self.__setattr__(key, None)


# class PusherMessageOpinions(PusherMessage):
#
#     def __init__(self, answers_amount: int):
#         super().__init__()
#         for i in range(1, answers_amount+1):
#             self.__setattr__(f'_answer_{i}', None)
#         # self._answer_1 = None
#         # self._answer_2 = None
#         # self._answer_3 = None
#         # self._answer_4 = None
#
#
# class PusherMessageTop5(PusherMessage):
#
#     def __init__(self):
#         super().__init__()
#         self._answer_1 = None
#         self._answer_2 = None
#         self._answer_3 = None
#         self._answer_4 = None
#         self._answer_5 = None
