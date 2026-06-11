# from game import Game
#
# if __name__ == '__main__':
#     game = Game()
#     game.run()
#
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game import Game
from entities import Bullet

# Nota: Coloque background.png, player.png e zombie1.png na pasta Assets/
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
game = Game(screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            b = Bullet(game.player.rect.centerx, game.player.rect.top)
            game.bullets.add(b)
            game.all_sprites.add(b)

    game.update()
    game.draw()
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()