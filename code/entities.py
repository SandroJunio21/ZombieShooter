import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED, YELLOW, BULLET_SPEED, PLAYER_PATH, \
    ZOMBIE_PATHS, ZOMBIE_SIZE, MYSTERY_BOX_PATH, MYSTERY_BOX_SIZE, MYSTERY_BOX_SPEED
from asset_loader import load_image

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image(PLAYER_PATH, (100, 100))
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += PLAYER_SPEED

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y -= BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()

class Zombie(pygame.sprite.Sprite):
    def __init__(self, speed, hp, image_path = None, image_size=None):
        super().__init__()
        if image_path is None:
            image_path = random.choice(ZOMBIE_PATHS)
        if image_size is None:
            image_size = ZOMBIE_SIZE
        self.image = load_image(image_path, image_size)
        self.rect = self.image.get_rect(x=random.randint(0, SCREEN_WIDTH - 40), y=-50)
        self.speed = speed
        self.hp = hp
        self.max_hp = hp
        self.has_damaged_player = False
        self.mask = pygame.mask.from_surface(self.image)
        self.just_passed_base = False

    def update(self):
        self.just_passed_base = False
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.just_passed_base = True
            self.rect.x = random.randint(0, SCREEN_WIDTH - 40)
            self.rect.y = -50
            self.has_damaged_player = False

class MysteryBox(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image(MYSTERY_BOX_PATH, MYSTERY_BOX_SIZE)
        self.rect = self.image.get_rect(x=random.randint(0, SCREEN_WIDTH - MYSTERY_BOX_SIZE[0]),
                                        y=-MYSTERY_BOX_SIZE[1])
        self.speed = MYSTERY_BOX_SPEED
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()