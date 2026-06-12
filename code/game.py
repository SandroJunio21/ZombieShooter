import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, ZOMBIE_SPEED, ZOMBIE_HP, WHITE
from background import Background
from entities import Player, Bullet, Zombie

class Game:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.zombies = pygame.sprite.Group()
        self.background = Background()
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.all_sprites.add(self.player)
        self.score = 0
        for _ in range(5): self.spawn_zombie()

    def spawn_zombie(self):
        z = Zombie(ZOMBIE_SPEED, ZOMBIE_HP)
        self.zombies.add(z)
        self.all_sprites.add(z)

    def update(self, keys):
        self.player.update(keys)
        self.bullets.update()
        self.zombies.update()
        hits = pygame.sprite.groupcollide(self.zombies, self.bullets, True, True, pygame.sprite.collide_mask)
        for hit in hits:
            self.score += 10
            self.spawn_zombie()

    def draw(self):
        self.screen.blit(self.background.image, (0,0))
        self.all_sprites.draw(self.screen)
        font = pygame.font.SysFont("Arial", 24)
        text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(text, (10, 10))