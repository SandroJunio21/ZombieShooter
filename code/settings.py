SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
#
COLORS = {
    'white': (255, 255, 255), 'black': (0, 0, 0), 'red': (200, 50, 50),
    'green': (50, 200, 50), 'blue': (50, 50, 200), 'gray': (100, 100, 100),
    'yellow': (255, 255, 0), 'purple': (128, 0, 128)
}

PLAYER_SPEED = 7
PLAYER_HP = 3
BULLET_SPEED = 10

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