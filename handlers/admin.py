# from aiogram import Router, Bot
# from aiogram.filters import Command, CommandObject
# from aiogram.types import Message
#
# from middleware import Admin
# from utils import FileManager
# from utils.enums import Path
#
# admin_router = Router()
# admin_router.message.middleware(Admin())
#
#
# @admin_router.message(Command('set'))
# async def command_start(message: Message, command: CommandObject, bot: Bot):
#     if command.args:
#         await FileManager.write(Path.PROMPT.value, 'main_prompt', data=command.args.strip())
#
#     await message.answer(
#         text='Done!',
#     )
