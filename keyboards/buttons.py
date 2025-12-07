class KeyboardButton:
    def __init__(self, text: str, callback, **kwargs):
        self.text = text
        self.callback_data = callback(
            **kwargs,
        )

    def as_kwargs(self):
        return self.__dict__
