import os
from enum import Enum


class Path(Enum):
    VOICE = os.path.join('data', 'voice')

