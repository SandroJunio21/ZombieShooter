# import pygame
# from settings import BG_PATH, SCREEN_WIDTH, SCREEN_HEIGHT
# from asset_loader import load_image
#
# class Background:
#     def __init__(self):
#         self.image = load_image(BG_PATH, (SCREEN_WIDTH, SCREEN_HEIGHT), alpha=False)
#
#     def draw(self, surface):
#         surface.blit(self.image, (0, 0))
#
# import pygame
# from asset_loader import load_image, create_fallback_background
# from settings import BG_PATH
#
#
# class Background(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.image = load_image(BG_PATH, (1280, 800))
#         if "magenta" in str(self.image.get_at((0,0))):
#             self.image = create_fallback_background()
#         self.rect = self.image.get_rect()

# import pygame
# from asset_loader import load_image, create_fallback_background
# from settings import BG_PATH, MENU_PATH
#
#
# class Background(pygame.sprite.Sprite):
#     """Classe para gerenciar o fundo do jogo."""
#
#     def __init__(self):
#         super().__init__()
#         try:
#             self.image = load_image(BG_PATH, (1280, 800))
#         except Exception:
#             self.image = create_fallback_background()
#
#         self.rect = self.image.get_rect()
#
#     def draw(self, surface):
#         """Desenha o fundo na superfície fornecida."""
#         surface.blit(self.image, self.rect)


import pygame
from settings import MENU_PATH, SCREEN_WIDTH, SCREEN_HEIGHT, BG_PATH
from asset_loader import load_image, create_fallback_background

class Background:
    def __init__(self, filename: str = BG_PATH):
        self.image = load_image(filename, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # Se a imagem for magenta (fallback), usa o gerador de fallback
        if self.image.get_at((0, 0)) == (255, 0, 255, 255):
            self.image = create_fallback_background()
        self.rect = self.image.get_rect()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
