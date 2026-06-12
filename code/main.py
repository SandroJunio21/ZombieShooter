# ===== main.py =====
import sys
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, MENU_PATH, MENU_MUSIC_PATH, GAME_MUSIC_PATH
from background import Background
from entities import Bullet
from game import Game

def play_music(path):
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)
    except Exception:
        pass

def draw_outlined_text(screen, text, font, color, pos):
    outline = font.render(text, True, (0, 0, 0))
    rendered = font.render(text, True, color)
    screen.blit(outline, (pos[0] - 2, pos[1] - 2))
    screen.blit(rendered, pos)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Menu")
    menu_background = Background(MENU_PATH)
    clock = pygame.time.Clock()
    pygame.mixer.init()
    current_music = None

    running = True
    state = "MENU"
    game = None

    options = ["Start", "Options", "Score", "Exit"]
    selected_index = 0
    font = pygame.font.SysFont("Arial", 60, bold=True)
    small_font = pygame.font.SysFont("Arial", 40, bold=True)

    while running:
        keys = pygame.key.get_pressed()
        if state in ["MENU", "OPTIONS"]:
            if current_music != "MENU":
                play_music(MENU_MUSIC_PATH)
                current_music = "MENU"
        elif state == "PLAYING":
            if current_music != "GAME":
                play_music(GAME_MUSIC_PATH)
                current_music = "GAME"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if state == "MENU" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    choice = options[selected_index]
                    if choice == "Start":
                        state = "PLAYING"
                        game = Game()
                    elif choice == "Options":
                        state = "OPTIONS"
                    elif choice == "Exit":
                        running = False

            elif state == "OPTIONS" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    state = "MENU"

            if state == "PLAYING" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    b = Bullet(game.player.rect.centerx, game.player.rect.top)
                    game.bullets.add(b)
                    game.all_sprites.add(b)

        if state == "MENU":
            menu_background.draw(screen)
            for i, option in enumerate(options):
                color = (255, 0, 0) if i == selected_index else WHITE
                rect = font.render(option, True, color).get_rect(center=(SCREEN_WIDTH // 2, 300 + i * 60))
                draw_outlined_text(screen, option, font, color, (rect.x, rect.y))

        elif state == "OPTIONS":
            menu_background.draw(screen)
            draw_outlined_text(screen, "Controles", font, WHITE, (60, 100))
            draw_outlined_text(screen, "Tecla de Espaco: Atira", small_font, WHITE, (60, 250))
            draw_outlined_text(screen, "Setas do teclado: Movimentacao", small_font, WHITE, (60, 300))
            draw_outlined_text(screen, "Tecla ESC: Pause", small_font, WHITE, (60, 350))
            draw_outlined_text(screen, "Pressione ENTER para voltar", small_font, (255, 255, 0), (60, 450))

        elif state == "PLAYING":
            game.update(keys)
            game.draw()
            if getattr(game, 'defeated', False):
                if pygame.time.get_ticks() - game.defeated_time > 1500:
                    state = "MENU"
                    game = None

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()

