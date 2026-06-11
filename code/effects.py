import pygame, random, math
from settings import COLORS

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((4, 4))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.vel = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
        self.life = 20

    def update(self):
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y
        self.life -= 1
        if self.life <= 0: self.kill()