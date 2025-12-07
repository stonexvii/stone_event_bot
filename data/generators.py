# from itertools import chain
# from random import choices, shuffle, choice
#
# from utils import FileManager
# from utils.enums import Path
#
#
# async def get_examples(file_name: str):
#     data_txt = await FileManager.read(Path.EXAMPLES.value, file_name)
#     normal, absurd = data_txt.split('\n\n')
#     normal = [f'<blockquote>{line.strip()}</blockquote>' for line in normal.split('\n')]
#     absurd = [f'<blockquote>{line.strip()}</blockquote>' for line in absurd.split('\n')]
#     collection = list(chain(choices(normal, k=2), choices(absurd, k=3)))
#     shuffle(collection)
#     result = '\n'.join(row for row in collection)
#     return result
#
#
# async def get_bot_message(file_name: str) -> str:
#     data_text = await FileManager.read(Path.BOT_MESSAGE.value, file_name)
#     return choice([line.strip() for line in data_text.split('\n')])
