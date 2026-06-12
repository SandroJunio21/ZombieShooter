import pygame
# from settings import BG_PATH, SCREEN_WIDTH, SCREEN_HEIGHT
# from asset_loader import load_image
#
# class Background:
#     def __init__(self):
#         self.image = load_image(BG_PATH, (SCREEN_WIDTH, SCREEN_HEIGHT), alpha=False)
#
#     def draw(self, surface):
#         surface.blit(self.image, (0, 0))

import pygame
from asset_loader import load_image, create_fallback_background

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("../Assets/background.png", (1280, 800))
        if "magenta" in str(self.image.get_at((0,0))):
            self.image = create_fallback_background()
        self.rect = self.image.get_rect()
