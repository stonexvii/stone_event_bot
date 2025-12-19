from database import requests


class CurrentEvent:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.id = None
        self.title = None
        self.questions = None

    async def activate(self):
        event = await requests.get_active_event()
        if event:
            self.id = event.id
            self.title = event.title
            self.questions = event.questions

    def get_question(self, question_id: int):
        return [question for question in self.questions if question.id == question_id][0]
