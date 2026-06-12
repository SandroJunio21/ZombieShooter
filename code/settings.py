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