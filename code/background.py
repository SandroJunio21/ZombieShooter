# import pygame, random
# from settings import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT
#
# class Background:
#     def draw(self, surface):
#         surface.fill((10, 10, 20))
#         pygame.draw.circle(surface, COLORS['white'], (700, 100), 40)
#         for _ in range(10):
#             pygame.draw.rect(surface, (20, 20, 30), (random.randint(0, 800), 500, 50, 100))

import pygame
from settings import BG_PATH, SCREEN_WIDTH, SCREEN_HEIGHT
from asset_loader import load_image

class Background:
    def __init__(self):
        self.image = load_image(BG_PATH, (SCREEN_WIDTH, SCREEN_HEIGHT), alpha=False)

    def draw(self, surface):
        surface.blit(self.image, (0, 0))
