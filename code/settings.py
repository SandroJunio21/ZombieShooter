import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
FPS = 60
#
COLORS = {
    'white': (255, 255, 255), 'black': (0, 0, 0), 'red': (200, 50, 50),
    'green': (50, 200, 50), 'blue': (50, 50, 200), 'gray': (100, 100, 100),
    'yellow': (255, 255, 0), 'purple': (128, 0, 128)
}


# Ajuste de dificuldade: altere valores abaixo
PHASES = {
    1: {'waves': 3, 'zombie_hp': 1, 'zombie_speed': 2, 'score': 10},
    2: {'waves': 3, 'zombie_hp': 2, 'zombie_speed': 3, 'score': 20},
    3: {'waves': 2, 'zombie_hp': 3, 'zombie_speed': 4, 'score': 50}
}

BG_PATH = '../Assets/background.png'
PLAYER_PATH = '../Assets/player.png'
ZOMBIE_PATH = '../Assets/zombie1.png'
MENU_PATH = '../Assets/Menu.png'
MENU_MUSIC_PATH = "../Assets/music_menu.mp3"
GAME_MUSIC_PATH = "../Assets/music_game.mp3"

# Tamanhos
PLAYER_SIZE = (72, 72)
ZOMBIE_SIZE = (64, 64)

PLAYER_SPEED = 8
PLAYER_HP = 3
BULLET_SPEED = 10
ZOMBIE_SPEED = 2
ZOMBIE_HP = 1

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
DARK_GRAY = (50, 50, 50)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

SHOT_COOLDOWN_MS: int = 140
PLAYER_TOUCH_DAMAGE = PLAYER_HP / 3 #10 #4
PLAYER_HIT_COOLDOWN_MS = 220 #800
HEALTH_BAR_BG_COLOR = (30, 30, 30) #DARK_GRAY
HEALTH_BAR_FILL_COLOR = (30, 30, 30) #(255, 0, 0)
HEALTH_BAR_BORDER_COLOR = WHITE
