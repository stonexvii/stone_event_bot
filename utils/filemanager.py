import os

import aiofiles


class FileManager:

    @staticmethod
    async def read(*args, **kwargs):
        path = os.path.join(*args) + '.txt'
        async with aiofiles.open(path, 'r', encoding='UTF-8') as file:
            response = await file.read()
        return response.strip().format(**kwargs)

    @staticmethod
    async def write(*args, data: str):
        path = os.path.join(*args) + '.txt'
        async with aiofiles.open(path, 'w', encoding='UTF-8') as file:
            await file.write(data)

    @staticmethod
    def read_txt(*args, with_kwargs: bool = True, **kwargs) -> str:
        path = os.path.join(*args) + '.txt'
        with open(path, 'r', encoding='UTF-8') as file:
            response = file.read()
        if with_kwargs:
            return response.strip().format(**kwargs)
        return response.strip()
