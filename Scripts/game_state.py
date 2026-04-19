from enum import Enum, auto


class GameState(Enum):
    MENU      = auto()
    PLAYING   = auto()
    PAUSED    = auto()
    WIN       = auto()
    GAME_OVER = auto()
