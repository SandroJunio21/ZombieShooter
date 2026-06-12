import pygame
import random
from settings import *
from entities import Player, Bullet, Zombie
from background import Background


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
        self.player_hp = float(PLAYER_HP)
        self.max_player_hp = float(PLAYER_HP)
        self.font = pygame.font.SysFont('Arial', 24)
        self.defeated_font = pygame.font.SysFont('Arial', 85)
        self.defeated = False
        self.defeated_time = None
        for _ in range(5):
            self.spawn_zombie()

    def spawn_zombie(self):
        zombie = Zombie(ZOMBIE_SPEED, ZOMBIE_HP)
        zombie.has_damaged_player = False
        self.zombies.add(zombie)
        self.all_sprites.add(zombie)

    def update(self, keys):
        if self.defeated:
            return
        self.player.update(keys)
        self.bullets.update()
        self.zombies.update()
        hits = pygame.sprite.groupcollide(self.zombies, self.bullets, True, True, pygame.sprite.collide_mask)
        for zombie in hits:
            self.score += 10
            self.spawn_zombie()
        zombie_hits = pygame.sprite.spritecollide(self.player, self.zombies, False, pygame.sprite.collide_mask)
        eligible_hits = [z for z in zombie_hits if not getattr(z, 'has_damaged_player', False)]
        if eligible_hits:
            for z in eligible_hits:
                z.has_damaged_player = True
            self.player_hp = max(0.0, self.player_hp - PLAYER_TOUCH_DAMAGE)
            if self.player_hp < 1:
                self.player_hp = 0.0
                self.defeated = True
                self.defeated_time = pygame.time.get_ticks()

    def draw(self):
        self.background.draw(self.screen)
        self.all_sprites.draw(self.screen)
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        bar_x, bar_y = SCREEN_WIDTH - 220, 10
        pygame.draw.rect(self.screen, HEALTH_BAR_BG_COLOR, (bar_x, bar_y, 200, 20))
        ratio = self.player_hp / self.max_player_hp
        fill_width = max(0, min(200, int(200 * ratio)))
        color = (0, 255, 0) if ratio > 0.6 else (255, 255, 0) if ratio > 0.3 else (255, 0, 0)
        pygame.draw.rect(self.screen, color, (bar_x, bar_y, fill_width, 20))
        pygame.draw.rect(self.screen, HEALTH_BAR_BORDER_COLOR, (bar_x, bar_y, 200, 20), 2)
        hp_text = self.font.render(f'Vida: {int(round(self.player_hp))}/{int(self.max_player_hp)}', True, WHITE)
        self.screen.blit(hp_text, (bar_x, bar_y + 25))
        if self.defeated:
            text = self.defeated_font.render('Derrotado', True, (255, 0, 0))
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, rect)