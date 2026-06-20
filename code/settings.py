import pygame

#resolution
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
FPS = 60

#colors
COLORS = {
    'white': (255, 255, 255), 'black': (0, 0, 0), 'red': (200, 50, 50),
    'green': (50, 200, 50), 'blue': (50, 50, 200), 'gray': (100, 100, 100),
    'yellow': (255, 255, 0), 'purple': (128, 0, 128)
}

# #phases
# PHASES = {
#     1: {'waves': 3, 'zombie_hp': 1, 'zombie_speed': 2, 'score': 10},
#     2: {'waves': 3, 'zombie_hp': 2, 'zombie_speed': 3, 'score': 20},
#     3: {'waves': 2, 'zombie_hp': 3, 'zombie_speed': 4, 'score': 50}
# }

#images
BG_PATH = '../Assets/background.png'
PLAYER_PATH = '../Assets/player.png'
ZOMBIE_PATH = '../Assets/zombie1.png'
ZOMBIE_PATHS = ["../Assets/zombie1.png","../Assets/zombie2.png"]
BOSS_ZOMBIE_PATH = "../Assets/zombie3.png"
MENU_PATH = '../Assets/Menu.png'
OPTIONS_PATH = '../Assets/options.png'
SCORE_PATH = '../Assets/score.png'
MYSTERY_BOX_PATH = '../Assets/caixa.png'

#music
MENU_MUSIC_PATH = "../Assets/music_menu.mp3"
GAME_MUSIC_PATH = "../Assets/music_game.mp3"

# Sizes
PLAYER_SIZE = (78, 78)
ZOMBIE_SIZE = (90, 90)
BOSS_ZOMBIE_SIZE = (190, 190)
MYSTERY_BOX_SIZE = (70, 70)

#speed
PLAYER_SPEED = 8
BULLET_SPEED = 10
ZOMBIE_SPEED = 2
MYSTERY_BOX_SPEED = 3

#life
ZOMBIE_HP = 1
PLAYER_HP = 3

#box
MYSTERY_BOX_SPAWN_MS = 10000
RAPID_FIRE_DURATION_MS = 15000


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
SPAWN_MARGIN = 50

SCORE_DB_PATH = "../Assets/scores.db"


