import os


class FileManager:
    @staticmethod
    def read_txt(*args, with_kwargs: bool = True, **kwargs) -> str:
        path = os.path.join(*args)
        if not path.endswith('.txt'):
            path += '.txt'
        with open(path, 'r', encoding='UTF-8') as file:
            response = file.read()
        if with_kwargs:
            return response.strip().format(**kwargs)
        return response.strip()


def question_from_text(data: str):
    quest_data = data.replace('\r', '').split('\n---\n')
    return [list(map(lambda x: x.strip(), question.split('\n'))) for question in quest_data]
