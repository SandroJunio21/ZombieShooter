import pygame, random
#from settings import COLORS, PLAYER_SPEED, BULLET_SPEED

# class Player(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.image = pygame.Surface((40, 30), pygame.SRCALPHA)
#         pygame.draw.polygon(self.image, COLORS['blue'], [(20, 0), (40, 30), (0, 30)])
#         self.rect = self.image.get_rect(center=(400, 550))
#         self.hp = 3
#         self.invul = 0
#
#     def update(self, keys):
#         if keys[pygame.K_LEFT] and self.rect.left > 0: self.rect.x -= PLAYER_SPEED
#         if keys[pygame.K_RIGHT] and self.rect.right < 800: self.rect.x += PLAYER_SPEED
#         if self.invul > 0: self.invul -= 1
#
# class Bullet(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__()
#         self.image = pygame.Surface((4, 10))
#         self.image.fill(COLORS['yellow'])
#         self.rect = self.image.get_rect(center=(x, y))
#
#     def update(self):
#         self.rect.y -= BULLET_SPEED
#         if self.rect.bottom < 0: self.kill()
#
# class Zombie(pygame.sprite.Sprite):
#     def __init__(self, speed, hp):
#         super().__init__()
#         self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
#         pygame.draw.circle(self.image, COLORS['green'], (15, 15), 15)
#         self.rect = self.image.get_rect(x=random.randint(0, 770), y=-50)
#         self.speed = speed
#         self.hp = hp
#
#     def update(self):
#         self.rect.y += self.speed
#         if self.rect.top > 600:
#             self.rect.y = -50
#             self.rect.x = random.randint(0, 770)

# import pygame
# import random
# from settings import PLAYER_SIZE, ZOMBIE_SIZE, PLAYER_PATH, ZOMBIE_PATH
# from asset_loader import load_image
#
# class Player(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__()
#         self.image = load_image(PLAYER_PATH, PLAYER_SIZE)
#         self.rect = self.image.get_rect(center=(x, y))
#         # self.mask = pygame.mask.from_surface(self.image)
#         self.speed = 8
#
#     def update(self, keys: pygame.key.ScancodeWrapper, screen_width: int):
#         if keys[pygame.K_LEFT] and self.rect.left > 0: self.rect.x -= self.speed
#         if keys[pygame.K_RIGHT] and self.rect.right < 800: self.rect.x += self.speed
#         # if keys[pygame.K_LEFT] and self.rect.left > 0:
#         #     self.rect.x -= self.speed
#         # if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
#         #     self.rect.x += self.speed
#
# class Zombie(pygame.sprite.Sprite):
#     def __init__(self, screen_width: int):
#         super().__init__()
#         self.image = load_image(ZOMBIE_PATH, ZOMBIE_SIZE)
#         self.rect = self.image.get_rect(x=random.randint(0, 736), y=-50)
#         self.speed = random.randint(2, 5)
#         # self.rect = self.image.get_rect(x=random.randint(0, screen_width - 50), y=-50)
#         # self.mask = pygame.mask.from_surface(self.image)
#         # self.speed = random.randint(2, 5)
#
#     def update(self):
#         self.rect.y += self.speed
#         if self.rect.top > 600:
#             self.rect.y = -50
#             self.rect.x = random.randint(0, 736)
#
# class Bullet(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__()
#         self.image = pygame.Surface((10, 20))
#         self.image.fill((255, 255, 0))
#         self.rect = self.image.get_rect(center=(x, y))
        # self.mask = pygame.mask.from_surface(self.image)

    # def update(self):
    #     self.rect.y -= 10
    #     if self.rect.bottom < 0:
    #         self.kill()

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
