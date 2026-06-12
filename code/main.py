import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE
from game import Game
from entities import Bullet

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    state = "MENU"
    game = None

    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if state == "MENU" and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                state = "PLAYING"
                game = Game()
            if state == "PLAYING" and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                b = Bullet(game.player.rect.centerx, game.player.rect.top)
                game.bullets.add(b)
                game.all_sprites.add(b)

        screen.fill((0,0,0))
        if state == "MENU":
            font = pygame.font.SysFont("Arial", 40)
            text = font.render("Pressione ESPAÇO para iniciar", True, WHITE)
            screen.blit(text, (410, 360))
        else:
            game.update(keys)
            game.draw()

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

if __name__ == '__main__':
    main()