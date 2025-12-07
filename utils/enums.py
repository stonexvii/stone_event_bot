import os
from enum import Enum


class Path(Enum):
    PROMPT = os.path.join('ai_gpt', 'prompts')
    # MESSAGE = os.path.join('data', 'message')
    VOICE = os.path.join('data', 'voice')
    MAIN_PROMPT = os.path.join('main_prompt')
    # START_COMMAND = os.path.join('data', 'message', 'start_command')
    # START_REMINDER = os.path.join('data', 'message', 'start_reminder')
    # START_GENERATE = os.path.join('data', 'message', 'start_generate')
    # EXAMPLES = os.path.join('data', 'examples')
    # BOT_MESSAGE = os.path.join('data', 'bot_messages')
