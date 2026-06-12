import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED, YELLOW, ZOMBIE_SPEED, PLAYER_PATH, ZOMBIE_PATH
from asset_loader import load_image

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image(PLAYER_PATH, (100, 100))
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0: self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH: self.rect.x += PLAYER_SPEED

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y -= 10
        if self.rect.bottom < 0: self.kill()

class Zombie(pygame.sprite.Sprite):
    def __init__(self, speed, hp):
        super().__init__()
        self.image = load_image(ZOMBIE_PATH, (100, 100))
        self.rect = self.image.get_rect(x=random.randint(0, SCREEN_WIDTH-40), y=-50)
        self.speed = speed
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.y = -50
            self.rect.x = random.randint(0, SCREEN_WIDTH-40)
