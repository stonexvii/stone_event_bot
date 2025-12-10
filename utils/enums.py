import os
from enum import Enum


class Path(Enum):
    PROMPT = os.path.join('ai_gpt', 'prompts')
    VOICE = os.path.join('data', 'voice')
    MAIN_PROMPT = os.path.join('main_prompt')
