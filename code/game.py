# import math
# import random
# import pygame
# from settings import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_HP, PLAYER_TOUCH_DAMAGE, WHITE, HEALTH_BAR_BG_COLOR, \
#     HEALTH_BAR_BORDER_COLOR, ZOMBIE_SPEED, ZOMBIE_HP, BOSS_ZOMBIE_PATH, BOSS_ZOMBIE_SIZE, MYSTERY_BOX_SPAWN_MS, \
#     RAPID_FIRE_DURATION_MS
# from entities import Player, Bullet, Zombie, MysteryBox
# from background import Background
#
# class Game:
#     def __init__(self):
#         self.screen = pygame.display.get_surface()
#         self.all_sprites = pygame.sprite.Group()
#         self.bullets = pygame.sprite.Group()
#         self.zombies = pygame.sprite.Group()
#         self.mystery_boxes = pygame.sprite.Group()
#         self.background = Background()
#         self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
#         self.all_sprites.add(self.player)
#         self.score = 0
#         self.level = 1
#         self.player_hp = float(PLAYER_HP)
#         self.max_player_hp = float(PLAYER_HP)
#         self.font = pygame.font.SysFont('World Conflict', 35)
#         self.hud_font = pygame.font.SysFont('World Conflict ', 30)
#         self.defeated_font = pygame.font.SysFont('28 Days Later', 140)
#         self.victory_font = pygame.font.SysFont('28 Days Later', 140)
#         self.defeated = False
#         self.victory = False
#         self.defeated_time = None
#         self.configure_level(1)
#         self.max_passed_zombies = 8
#         self.passed_zombies = 0
#         self.mystery_box_spawn_time = pygame.time.get_ticks() + MYSTERY_BOX_SPAWN_MS
#         self.rapid_fire_end_time = 0
#         self.power_message = ""
#         self.power_message_end_time = 0
#
#     def spawn_zombie(self, speed=None, hp=None, image_path=None, image_size=None):
#         s = speed if speed is not None else ZOMBIE_SPEED
#         h = hp if hp is not None else ZOMBIE_HP
#         zombie = Zombie(s, h, image_path,image_size)
#         self.zombies.add(zombie)
#         self.all_sprites.add(zombie)
#
#     def spawn_mystery_box(self):
#         if len(self.mystery_boxes) == 0:
#             box = MysteryBox()
#             self.mystery_boxes.add(box)
#             self.all_sprites.add(box)
#
#     def apply_random_power(self):
#         if random.choice([True, False]):
#             self.grant_extra_life()
#         else:
#             self.grant_rapid_fire()
#
#     def grant_extra_life(self):
#         self.max_player_hp += 1
#         self.player_hp += 1
#         self.show_power_message("Vida Extra +1!")
#
#     def grant_rapid_fire(self):
#         self.rapid_fire_end_time = pygame.time.get_ticks() + RAPID_FIRE_DURATION_MS
#         self.show_power_message("Rajada de Tiros!")
#
#     def is_rapid_fire_active(self):
#         return pygame.time.get_ticks() < self.rapid_fire_end_time
#
#     def get_rapid_fire_seconds_left(self):
#         if not self.is_rapid_fire_active():
#             return 0
#         return int((self.rapid_fire_end_time - pygame.time.get_ticks()) / 1000) + 1
#
#     def show_power_message(self, text):
#         self.power_message = text
#         self.power_message_end_time = pygame.time.get_ticks() + 2000
#
#     def configure_level(self, level):
#         self.level = level
#         if level == 1:
#             for _ in range(8): self.spawn_zombie()
#         elif level == 2:
#             for _ in range(11): self.spawn_zombie()
#         elif level == 3:
#             self.spawn_zombie(speed=max(1, ZOMBIE_SPEED - 1), hp=ZOMBIE_HP * 30,  image_path=BOSS_ZOMBIE_PATH, image_size=BOSS_ZOMBIE_SIZE )
#
#     def update_level(self):
#         if self.score >= 1500 and self.level < 3:
#             self.configure_level(3)
#         elif self.score >= 800 and self.level < 2:
#             self.configure_level(2)
#
#     def maintain_zombie_count(self):
#         if self.victory: return
#         if self.level == 1 and len(self.zombies) < 8: self.spawn_zombie()
#         elif self.level == 2 and len(self.zombies) < 11: self.spawn_zombie()
#
#     def update(self, keys):
#         if self.defeated or self.victory: return
#         self.player.update(keys)
#         self.bullets.update()
#         self.zombies.update()
#         self.mystery_boxes.update()
#         now = pygame.time.get_ticks()
#         if now >= self.mystery_box_spawn_time and len(self.mystery_boxes) == 0:
#             self.spawn_mystery_box()
#             self.mystery_box_spawn_time = now + MYSTERY_BOX_SPAWN_MS
#         for zombie in self.zombies:
#             if zombie.just_passed_base:
#                 self.passed_zombies += 1
#                 zombie.just_passed_base = False
#         if self.passed_zombies >= self.max_passed_zombies:
#             self.defeated = True
#             self.defeated_time = pygame.time.get_ticks()
#         for bullet in list(self.bullets):
#             zombie_hits = pygame.sprite.spritecollide(bullet, self.zombies, False, pygame.sprite.collide_mask)
#             if zombie_hits:
#                 zombie = zombie_hits[0]
#                 bullet.kill()
#                 zombie.hp -= 1
#                 if zombie.hp <= 0:
#                     zombie.kill()
#                     self.score += 10
#                     if self.level == 3 and len(self.zombies) == 0:
#                         self.victory = True
#                     else:
#                         self.update_level()
#                         self.maintain_zombie_count()
#                 continue
#             box_hits = pygame.sprite.spritecollide(bullet, self.mystery_boxes, False, pygame.sprite.collide_mask)
#             if box_hits:
#                 box = box_hits[0]
#                 bullet.kill()
#                 box.kill()
#                 self.apply_random_power()
#                 self.mystery_box_spawn_time = now + MYSTERY_BOX_SPAWN_MS
#         zombie_hits = pygame.sprite.spritecollide(self.player, self.zombies, False, pygame.sprite.collide_mask)
#         eligible_hits = [z for z in zombie_hits if not getattr(z, 'has_damaged_player', False)]
#         for z in eligible_hits:
#             z.has_damaged_player = True
#             self.player_hp = max(0.0, self.player_hp - PLAYER_TOUCH_DAMAGE)
#             if self.player_hp < 1:
#                 self.player_hp = 0.0
#                 self.defeated = True
#                 self.defeated_time = pygame.time.get_ticks()
#
#     def draw(self):
#         self.background.draw(self.screen)
#         self.all_sprites.draw(self.screen)
#         self.draw_outlined_text_top_left(f'Score: {self.score}', self.hud_font, (10, 10), WHITE, outline_width=2)
#         self.draw_outlined_text_top_left(f'Level: {self.level}', self.hud_font, (10, 40), WHITE, outline_width=2)
#         self.draw_outlined_text_top_left(f'Invasão Zumbi: {self.passed_zombies}/{self.max_passed_zombies}', self.hud_font,
#                                          (10, 70), WHITE, outline_width=2)
#         if self.is_rapid_fire_active():
#             self.draw_outlined_text_top_left(f'Habilidade: Rajada dupla ({self.get_rapid_fire_seconds_left()}s)', self.hud_font,
#                                              (10, 100), WHITE, outline_width=2)
#         else:
#             self.draw_outlined_text_top_left('Habilidade: Nenhuma', self.hud_font, (10, 100), WHITE, outline_width=2)
#         bar_x, bar_y = SCREEN_WIDTH - 220, 10
#         pygame.draw.rect(self.screen, HEALTH_BAR_BG_COLOR, (bar_x, bar_y, 200, 20))
#         ratio = self.player_hp / self.max_player_hp
#         fill_width = max(0, min(200, int(200 * ratio)))
#         color = (0, 255, 0) if ratio > 0.6 else (255, 255, 0) if ratio > 0.3 else (255, 0, 0)
#         pygame.draw.rect(self.screen, color, (bar_x, bar_y, fill_width, 20))
#         pygame.draw.rect(self.screen, HEALTH_BAR_BORDER_COLOR, (bar_x, bar_y, 200, 20), 2)
#         self.draw_outlined_text_top_left(f'Vida: {int(round(self.player_hp))}/{int(self.max_player_hp)}', self.font, (bar_x, bar_y + 25), WHITE, outline_width=2)
#         now = pygame.time.get_ticks()
#         if self.power_message and now < self.power_message_end_time:
#             self.draw_power_message_effect(self.power_message, (SCREEN_WIDTH // 2, 50))
#         if self.defeated:
#             self.draw_outlined_text('Derrotado', self.defeated_font, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
#                                     (255, 0, 0))
#         elif getattr(self, 'victory', False):
#             self.draw_outlined_text('Vitoria', self.defeated_font, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (0, 255, 0))
#
#     def draw_power_message_effect(self, text, center, color=(255, 255, 0), outline_color=(0, 0, 0), shadow_color=(0, 0, 0)):
#         now = pygame.time.get_ticks()
#         pulse = 1.0 + 0.22 * math.sin(now / 160.0)
#         base_size = 60
#         scaled_size = max(1, int(base_size * pulse))
#         font = pygame.font.SysFont('World Conflict ', scaled_size) if scaled_size != base_size else self.font
#         shadow_offset = (3, 3)
#         shadow = font.render(text, True, shadow_color)
#         shadow_rect = shadow.get_rect(center=(center[0] + shadow_offset[0], center[1] + shadow_offset[1]))
#         self.screen.blit(shadow, shadow_rect)
#         outline = font.render(text, True, outline_color)
#         outline_rect = outline.get_rect(center=center)
#         for dx in range(-2, 3):
#             for dy in range(-2, 3):
#                 if dx == 0 and dy == 0:
#                     continue
#                 self.screen.blit(outline, outline.get_rect(center=(outline_rect.centerx + dx, outline_rect.centery + dy)))
#         rendered = font.render(text, True, color)
#         rendered_rect = rendered.get_rect(center=center)
#         self.screen.blit(rendered, rendered_rect)
#
#     def draw_outlined_text(self, text, font, center, color, outline_color=(0, 0, 0), outline_width=3):
#         rendered = font.render(text, True, color)
#         rect = rendered.get_rect(center=center)
#         outline = font.render(text, True, outline_color)
#         for dx in range(-outline_width, outline_width + 1):
#             for dy in range(-outline_width, outline_width + 1):
#                 if dx == 0 and dy == 0:
#                     continue
#                 self.screen.blit(outline, outline.get_rect(center=(rect.centerx + dx, rect.centery + dy)))
#                 self.screen.blit(rendered, rect)
#
#     def draw_outlined_text_top_left(self, text, font, topleft, color, outline_color=(0, 0, 0),
#                                     outline_width=2):
#         rendered = font.render(text, True, color)
#         rect = rendered.get_rect(topleft=topleft)
#         outline = font.render(text, True, outline_color)
#         for dx in range(-outline_width, outline_width + 1):
#             for dy in range(-outline_width, outline_width + 1):
#                 if dx == 0 and dy == 0:
#                     continue
#
#                 self.screen.blit(outline, outline.get_rect(center=(rect.centerx + dx, rect.centery + dy)))
#         self.screen.blit(rendered, rect)



import math
import random
import pygame
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_HP, PLAYER_TOUCH_DAMAGE, WHITE, HEALTH_BAR_BG_COLOR, \
    HEALTH_BAR_BORDER_COLOR, ZOMBIE_SPEED, ZOMBIE_HP, BOSS_ZOMBIE_PATH, BOSS_ZOMBIE_SIZE, MYSTERY_BOX_SPAWN_MS, \
    RAPID_FIRE_DURATION_MS
from .entities import Player, Bullet, Zombie, MysteryBox
from .background import Background

class Game:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.zombies = pygame.sprite.Group()
        self.mystery_boxes = pygame.sprite.Group()
        self.background = Background()
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.all_sprites.add(self.player)
        self.score = 0
        self.level = 1
        self.player_hp = float(PLAYER_HP)
        self.max_player_hp = float(PLAYER_HP)
        self.font = pygame.font.SysFont('World Conflict', 35)
        self.hud_font = pygame.font.SysFont('World Conflict ', 30)
        self.defeated_font = pygame.font.SysFont('28 Days Later', 140)
        self.victory_font = pygame.font.SysFont('28 Days Later', 140)
        self.defeated = False
        self.victory = False
        self.defeated_time = None
        self.configure_level(1)
        self.max_passed_zombies = 8
        self.passed_zombies = 0
        self.mystery_box_spawn_time = pygame.time.get_ticks() + MYSTERY_BOX_SPAWN_MS
        self.rapid_fire_end_time = 0
        self.power_message = ""
        self.power_message_end_time = 0
    def spawn_zombie(self, speed=None, hp=None, image_path=None, image_size=None):
        s = speed if speed is not None else ZOMBIE_SPEED
        h = hp if hp is not None else ZOMBIE_HP
        zombie = Zombie(s, h, image_path,image_size)
        self.zombies.add(zombie)
        self.all_sprites.add(zombie)
    def spawn_mystery_box(self):
        if len(self.mystery_boxes) == 0:
            box = MysteryBox()
            self.mystery_boxes.add(box)
            self.all_sprites.add(box)
    def apply_random_power(self):
        if random.choice([True, False]):
            self.grant_extra_life()
        else:
            self.grant_rapid_fire()
    def grant_extra_life(self):
        self.max_player_hp += 1
        self.player_hp += 1
        self.show_power_message("Vida Extra +1!")
    def grant_rapid_fire(self):
        self.rapid_fire_end_time = pygame.time.get_ticks() + RAPID_FIRE_DURATION_MS
        self.show_power_message("Rajada de Tiros!")
    def is_rapid_fire_active(self):
        return pygame.time.get_ticks() < self.rapid_fire_end_time
    def get_rapid_fire_seconds_left(self):
        if not self.is_rapid_fire_active():
            return 0
        return int((self.rapid_fire_end_time - pygame.time.get_ticks()) / 1000) + 1
    def show_power_message(self, text):
        self.power_message = text
        self.power_message_end_time = pygame.time.get_ticks() + 2000
    def configure_level(self, level):
        self.level = level
        if level == 1:
            for _ in range(8): self.spawn_zombie()
        elif level == 2:
            for _ in range(11): self.spawn_zombie()
        elif level == 3:
            self.spawn_zombie(speed=max(1, ZOMBIE_SPEED - 1), hp=ZOMBIE_HP * 30,  image_path=BOSS_ZOMBIE_PATH, image_size=BOSS_ZOMBIE_SIZE )
    def update_level(self):
        if self.score >= 1500 and self.level < 3:
            self.configure_level(3)
        elif self.score >= 800 and self.level < 2:
            self.configure_level(2)
    def maintain_zombie_count(self):
        if self.victory: return
        if self.level == 1 and len(self.zombies) < 8: self.spawn_zombie()
        elif self.level == 2 and len(self.zombies) < 11: self.spawn_zombie()
    def update(self, keys):
        if self.defeated or self.victory: return
        self.player.update(keys)
        self.bullets.update()
        self.zombies.update()
        self.mystery_boxes.update()
        now = pygame.time.get_ticks()
        if now >= self.mystery_box_spawn_time and len(self.mystery_boxes) == 0:
            self.spawn_mystery_box()
            self.mystery_box_spawn_time = now + MYSTERY_BOX_SPAWN_MS
        for zombie in self.zombies:
            if zombie.just_passed_base:
                self.passed_zombies += 1
                zombie.just_passed_base = False
        if self.passed_zombies >= self.max_passed_zombies:
            self.defeated = True
            self.defeated_time = pygame.time.get_ticks()
        for bullet in list(self.bullets):
            zombie_hits = pygame.sprite.spritecollide(bullet, self.zombies, False, pygame.sprite.collide_mask)
            if zombie_hits:
                zombie = zombie_hits[0]
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
                continue
            box_hits = pygame.sprite.spritecollide(bullet, self.mystery_boxes, False, pygame.sprite.collide_mask)
            if box_hits:
                box = box_hits[0]
                bullet.kill()
                box.kill()
                self.apply_random_power()
                self.mystery_box_spawn_time = now + MYSTERY_BOX_SPAWN_MS
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
        self.draw_outlined_text_top_left(f'Score: {self.score}', self.hud_font, (10, 10), WHITE, outline_width=2)
        self.draw_outlined_text_top_left(f'Level: {self.level}', self.hud_font, (10, 40), WHITE, outline_width=2)
        self.draw_outlined_text_top_left(f'Invasão Zumbi: {self.passed_zombies}/{self.max_passed_zombies}', self.hud_font, (10, 70), WHITE, outline_width=2)
        if self.is_rapid_fire_active():
            self.draw_outlined_text_top_left(f'Habilidade: Rajada dupla ({self.get_rapid_fire_seconds_left()}s)', self.hud_font, (10, 100), WHITE, outline_width=2)
        else:
            self.draw_outlined_text_top_left('Habilidade: Nenhuma', self.hud_font, (10, 100), WHITE, outline_width=2)
        bar_x, bar_y = SCREEN_WIDTH - 220, 10
        pygame.draw.rect(self.screen, HEALTH_BAR_BG_COLOR, (bar_x, bar_y, 200, 20))
        ratio = self.player_hp / self.max_player_hp
        fill_width = max(0, min(200, int(200 * ratio)))
        color = (0, 255, 0) if ratio > 0.6 else (255, 255, 0) if ratio > 0.3 else (255, 0, 0)
        pygame.draw.rect(self.screen, color, (bar_x, bar_y, fill_width, 20))
        pygame.draw.rect(self.screen, HEALTH_BAR_BORDER_COLOR, (bar_x, bar_y, 200, 20), 2)
        self.draw_outlined_text_top_left(f'Vida: {int(round(self.player_hp))}/{int(self.max_player_hp)}', self.font, (bar_x, bar_y + 25), WHITE, outline_width=2)
        now = pygame.time.get_ticks()
        if self.power_message and now < self.power_message_end_time:
            self.draw_power_message_effect(self.power_message, (SCREEN_WIDTH // 2, 50))
        if self.defeated:
            self.draw_outlined_text('Derrotado', self.defeated_font, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (255, 0, 0))
        elif getattr(self, 'victory', False):
            self.draw_outlined_text('Vitoria', self.defeated_font, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (0, 255, 0))
    def draw_power_message_effect(self, text, center, color=(255, 255, 0), outline_color=(0, 0, 0), shadow_color=(0, 0, 0)):
        now = pygame.time.get_ticks()
        pulse = 1.0 + 0.22 * math.sin(now / 160.0)
        base_size = 60
        scaled_size = max(1, int(base_size * pulse))
        font = pygame.font.SysFont('World Conflict ', scaled_size) if scaled_size != base_size else self.font
        shadow_offset = (3, 3)
        shadow = font.render(text, True, shadow_color)
        shadow_rect = shadow.get_rect(center=(center[0] + shadow_offset[0], center[1] + shadow_offset[1]))
        self.screen.blit(shadow, shadow_rect)
        outline = font.render(text, True, outline_color)
        outline_rect = outline.get_rect(center=center)
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx == 0 and dy == 0:
                    continue
                self.screen.blit(outline, outline.get_rect(center=(outline_rect.centerx + dx, outline_rect.centery + dy)))
        rendered = font.render(text, True, color)
        rendered_rect = rendered.get_rect(center=center)
        self.screen.blit(rendered, rendered_rect)
    def draw_outlined_text(self, text, font, center, color, outline_color=(0, 0, 0), outline_width=3):
        rendered = font.render(text, True, color)
        rect = rendered.get_rect(center=center)
        outline = font.render(text, True, outline_color)
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx == 0 and dy == 0:
                    continue
                self.screen.blit(outline, outline.get_rect(center=(rect.centerx + dx, rect.centery + dy)))
        self.screen.blit(rendered, rect)
    def draw_outlined_text_top_left(self, text, font, topleft, color, outline_color=(0, 0, 0), outline_width=2):
        rendered = font.render(text, True, color)
        rect = rendered.get_rect(topleft=topleft)
        outline = font.render(text, True, outline_color)
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx == 0 and dy == 0:
                    continue
                self.screen.blit(outline, outline.get_rect(topleft=(rect.x + dx, rect.y + dy)))
        self.screen.blit(rendered, rect)