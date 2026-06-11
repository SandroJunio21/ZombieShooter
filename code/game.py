import pygame, sys
from settings import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT
from states import GameState
from entities import Player, Bullet, Zombie
from background import Background
from waves import WaveManager
from ui import draw_text

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.state = GameState.MENU
        self.player = Player()
        self.bullets = pygame.sprite.Group()
        self.zombies = pygame.sprite.Group()
        self.bg = Background()
        self.wm = WaveManager()
        self.score = 0
        self.all_sprites = pygame.sprite.Group(self.player)
        self.font = pygame.font.SysFont("Arial", 30)
        for _ in range(5): self.spawn_zombie()

    def spawn_zombie(self):
        z = Zombie(SCREEN_WIDTH)
        zombies.add(z)
        all_sprites.add(z)

    # for _ in range(5): spawn_zombie()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if self.state == GameState.MENU and event.key == pygame.K_SPACE: self.state = GameState.PLAYING
                if self.state in [GameState.GAME_OVER, GameState.VICTORY] and event.key == pygame.K_r: self.__init__()

    def update(self):
        self.all_sprites.update()
        hits = pygame.sprite.groupcollide(self.zombies, self.bullets, True, True)
        if self.state == GameState.PLAYING:
            keys = pygame.key.get_pressed()
            self.player.update(keys)
            if keys[pygame.K_SPACE] and pygame.time.get_ticks() % 10 == 0: self.bullets.add(Bullet(self.player.rect.centerx, self.player.rect.top))
            self.bullets.update()
            self.zombies.update()
            if len(self.zombies) < 5: self.zombies.add(Zombie(2, 1))
            hits = pygame.sprite.groupcollide(self.bullets, self.zombies, True, False)
            # for hit in hits:
            #     for z in hits[hit]:
            #         z.hp -= 1
            #         if z.hp <= 0: z.kill(); self.score += 10
            for hit in hits:
                self.score += 10
                self.spawn_zombie()

    def draw(self):
        self.bg.draw(self.screen)
        if self.state == GameState.MENU: draw_text(self.screen, "APOCALYPSE - PRESS SPACE", 40, 200, 300)
        elif self.state == GameState.PLAYING:
            self.screen.blit(self.player.image, self.player.rect)
            self.bullets.draw(self.screen)
            self.zombies.draw(self.screen)
            draw_text(self.screen, f"Score: {self.score}", 20, 10, 10)
        pygame.display.flip()

# ===== main.py =====
from game import Game

if __name__ == '__main__':
    game = Game()
    game.run()

import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from background import Background
from entities import Player, Zombie, Bullet

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

background = Background()
player = Player(400, 500)
zombies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group(player, *zombies)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            b = Bullet(player.rect.centerx, player.rect.top)
            bullets.add(b)
            all_sprites.add(b)

    all_sprites.update()
    player.update(pygame.key.get_pressed(), SCREEN_WIDTH)

    # Colisao precisa com mascara
    hits = pygame.sprite.groupcollide(bullets, zombies, True, True, pygame.sprite.collide_mask)

pygame.quit()