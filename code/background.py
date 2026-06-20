import pygame
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, BG_PATH
from .asset_loader import load_image, create_fallback_background

class Background:

    def __init__(self, filename: str = BG_PATH):
        self.image = load_image(filename, (SCREEN_WIDTH, SCREEN_HEIGHT))
        if self.image.get_at((0, 0)) == (255, 0, 255, 255):
            self.image = create_fallback_background()
        self.rect = self.image.get_rect()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
