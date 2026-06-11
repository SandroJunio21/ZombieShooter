import pygame
from settings import COLORS

def draw_text(surface, text, size, x, y, color=COLORS['white']):
    font = pygame.font.SysFont('Arial', size)
    surf = font.render(text, True, color)
    surface.blit(surf, (x, y))