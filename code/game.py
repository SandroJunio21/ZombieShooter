import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_HP, PLAYER_TOUCH_DAMAGE, WHITE, HEALTH_BAR_BG_COLOR, \
    HEALTH_BAR_BORDER_COLOR, ZOMBIE_SPEED, ZOMBIE_HP, BOSS_ZOMBIE_PATH, BOSS_ZOMBIE_SIZE
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
        self.level = 1
        self.player_hp = float(PLAYER_HP)
        self.max_player_hp = float(PLAYER_HP)
        self.font = pygame.font.SysFont('World Conflict ', 35)
        self.defeated_font = pygame.font.SysFont('28 Days Later', 140)
        self.victory_font = pygame.font.SysFont('28 Days Later', 140)
        self.defeated = False
        self.victory = False
        self.defeated_time = None
        self.configure_level(1)

    def spawn_zombie(self, speed=None, hp=None, image_path=None, image_size=None):
        s = speed if speed is not None else ZOMBIE_SPEED
        h = hp if hp is not None else ZOMBIE_HP
        zombie = Zombie(s, h, image_path,image_size)
        self.zombies.add(zombie)
        self.all_sprites.add(zombie)

    def configure_level(self, level):
        self.level = level
        if level == 1:
            for _ in range(5): self.spawn_zombie()
        elif level == 2:
            for _ in range(8): self.spawn_zombie()
        elif level == 3:
            self.spawn_zombie(speed=max(1, ZOMBIE_SPEED - 1), hp=ZOMBIE_HP * 15,  image_path=BOSS_ZOMBIE_PATH, image_size=BOSS_ZOMBIE_SIZE )

    def update_level(self):
        if self.score >= 300 and self.level < 3:
            self.configure_level(3)
        elif self.score >= 100 and self.level < 2:
            self.configure_level(2)

    def maintain_zombie_count(self):
        if self.victory: return
        if self.level == 1 and len(self.zombies) < 5: self.spawn_zombie()
        elif self.level == 2 and len(self.zombies) < 8: self.spawn_zombie()

    def update(self, keys):
        if self.defeated or self.victory: return
        self.player.update(keys)
        self.bullets.update()
        self.zombies.update()
        for bullet in list(self.bullets):
            hits = pygame.sprite.spritecollide(bullet, self.zombies, False, pygame.sprite.collide_mask)
            if hits:
                zombie = hits[0]
                bullet.kill()
                zombie.hp -= 1
                if zombie.hp <= 0:
                    zombie.kill()
                    self.score += 10
                    if self.level == 3 and len(self.zombies) == 0:
                        self.victory = True
                    else:
                        self.update_level()
                        self.maintain_zombie_count()
        zombie_hits = pygame.sprite.spritecollide(self.player, self.zombies, False, pygame.sprite.collide_mask)
        eligible_hits = [z for z in zombie_hits if not getattr(z, 'has_damaged_player', False)]
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
        level_text = self.font.render(f'Level: {self.level}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 40))
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
            self.draw_outlined_text('Derrotado', self.defeated_font, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                                    (255, 0, 0))
        elif getattr(self, 'victory', False):
            self.draw_outlined_text('Vitoria', self.defeated_font, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (0, 255, 0))

    def draw_outlined_text(self, text, font, center, color, outline_color=(0, 0, 0), outline_width=2):
        rendered = font.render(text, True, color)
        rect = rendered.get_rect(center=center)
        outline = font.render(text, True, outline_color)
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx == 0 and dy == 0:
                    continue
                self.screen.blit(outline, outline.get_rect(center=(rect.centerx + dx, rect.centery + dy)))
        self.screen.blit(rendered, rect)
