from enum import Enum, auto

class GameState(Enum):
    MENU = auto()
    TRANSITION = auto()
    PLAYING = auto()
    GAME_OVER = auto()
    VICTORY = auto()
