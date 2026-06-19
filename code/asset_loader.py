import pygame
from settings import DARK_GRAY

def load_image(path: str, size: tuple = None, alpha: bool = True, fallback_size=(64, 64), fallback_color=(255, 0, 255)) -> pygame.Surface:
    """Carrega imagem ou cria surface de erro caso nao encontrada."""
    try:
        image = pygame.image.load(path)
        if alpha: image = image.convert_alpha()
        else: image = image.convert()
        if size: image = pygame.transform.scale(image, size)
        return image
    except (pygame.error, FileNotFoundError):
        surf = pygame.Surface(size or fallback_size)
        surf.fill(fallback_color)
        return surf

def create_fallback_background():
    surf = pygame.Surface((1280, 800))
    surf.fill(DARK_GRAY)
    for i in range(0, 800, 50):
        pygame.draw.line(surf, (70, 70, 70), (i, 0), (i, 600))
    for i in range(0, 600, 50):
        pygame.draw.line(surf, (70, 70, 70), (0, i), (800, i))
    return surf

