import sys
import sqlite3
import datetime
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, MENU_PATH, MENU_MUSIC_PATH, GAME_MUSIC_PATH, SCORE_PATH, \
    OPTIONS_PATH, SCORE_DB_PATH, YELLOW
from background import Background
from entities import Bullet
from game import Game


# def play_music(path):
#     try:
#         pygame.mixer.music.load(path)
#         pygame.mixer.music.play(-1)
#     except Exception:
#         pass
#
#
# def draw_outlined_text(screen, text, font, color, pos):
#     outline = font.render(text, True, (0, 0, 0))
#     rendered = font.render(text, True, color)
#     screen.blit(outline, (pos[0] - 2, pos[1] - 2))
#     screen.blit(rendered, pos)
#
#
# def draw_shadow_text(screen, text, font, color, pos, shadow_offset=(10, 10)):
#     shadow = font.render(text, True, (30, 30, 30))
#     outline = font.render(text, True, (0, 0, 0))
#     rendered = font.render(text, True, color)
#     screen.blit(shadow, (pos[0] + shadow_offset[0], pos[1] + shadow_offset[1]))
#     screen.blit(outline, (pos[0] - 2, pos[1] - 2))
#     screen.blit(rendered, pos)
#
#
# def init_score_db():
#     conn = sqlite3.connect(SCORE_DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS scores (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             player_name TEXT NOT NULL,
#             score INTEGER NOT NULL,
#             played_date TEXT NOT NULL,
#             played_time TEXT NOT NULL,
#             played_at TEXT NOT NULL
#         )
#     """)
#     conn.commit()
#     conn.close()
#
#
# def save_score(player_name, score):
#     now = datetime.datetime.now()
#     played_date = now.strftime("%d/%m/%Y")
#     played_time = now.strftime("%H:%M:%S")
#     played_at = now.isoformat()
#     conn = sqlite3.connect(SCORE_DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("""
#         INSERT INTO scores (player_name, score, played_date, played_time, played_at)
#         VALUES (?, ?, ?, ?, ?)
#     """, (player_name, score, played_date, played_time, played_at))
#     conn.commit()
#     conn.close()
#
#
# def get_top_scores(limit=10):
#     conn = sqlite3.connect(SCORE_DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT player_name, score, played_date, played_time
#         FROM scores
#         ORDER BY score DESC, played_at DESC
#         LIMIT ?
#     """, (limit,))
#     rows = cursor.fetchall()
#     conn.close()
#     return rows
#
#
# def main():
#     pygame.init()
#     screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#     pygame.display.set_caption("Game Menu")
#     menu_background = Background(MENU_PATH)
#     options_background = Background(OPTIONS_PATH)
#     score_background = Background(SCORE_PATH)
#     clock = pygame.time.Clock()
#     pygame.mixer.init()
#     current_music = None
#
#     init_score_db()
#
#     running = True
#     state = "MENU"
#     game = None
#
#     options = ["Start", "Options", "Score", "Exit"]
#     selected_index = 0
#     font = pygame.font.SysFont("28 Days Later", 70, bold=False)
#     small_font = pygame.font.SysFont("Arial", 40, bold=False)
#     pause_font = pygame.font.SysFont("28 Days Later", 80, bold=False)
#     title_font = pygame.font.SysFont("28 Days Later", 145, bold=False)
#     popup_font = pygame.font.SysFont("Arial", 60, bold=False)
#     input_font = pygame.font.SysFont("Arial", 50, bold=False)
#     score_title_font = pygame.font.SysFont("28 Days Later", 80, bold=False)
#     score_list_font = pygame.font.SysFont("Arial", 32, bold=False)
#
#     end_popup_active = False
#     player_name_input = ""
#     end_result_text = ""
#     score_saved = False
#     top_scores = []
#
#     while running:
#         keys = pygame.key.get_pressed()
#         if state in ["MENU", "OPTIONS", "SCORE"]:
#             if current_music != "MENU":
#                 play_music(MENU_MUSIC_PATH)
#                 current_music = "MENU"
#         elif state in ["PLAYING", "PAUSED"]:
#             if current_music != "GAME":
#                 play_music(GAME_MUSIC_PATH)
#                 current_music = "GAME"
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#
#             if end_popup_active:
#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_RETURN:
#                         if player_name_input.strip():
#                             save_score(player_name_input.strip().upper(), game.score)
#                             score_saved = True
#                             end_popup_active = False
#                             player_name_input = ""
#                             end_result_text = ""
#                             state = "MENU"
#                             game = None
#                         elif event.key == pygame.K_ESCAPE:
#                             end_popup_active = False
#                             player_name_input = ""
#                             end_result_text = ""
#                             score_saved = False
#                             state = "MENU"
#                             game = None
#                     elif event.key == pygame.K_BACKSPACE:
#                         player_name_input = player_name_input[:-1]
#                     elif event.unicode.isalnum():
#                         if len(player_name_input) < 10:
#                             player_name_input += event.unicode.upper()
#                 continue
#
#             if state == "MENU" and event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_UP:
#                     selected_index = (selected_index - 1) % len(options)
#                 elif event.key == pygame.K_DOWN:
#                     selected_index = (selected_index + 1) % len(options)
#                 elif event.key == pygame.K_RETURN:
#                     choice = options[selected_index]
#                     if choice == "Start":
#                         state = "PLAYING"
#                         game = Game()
#                     elif choice == "Options":
#                         state = "OPTIONS"
#                     elif choice == "Score":
#                         state = "SCORE"
#                         top_scores = get_top_scores(10)
#                     elif choice == "Exit":
#                         running = False
#
#             elif state == "OPTIONS" and event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
#                     state = "MENU"
#
#             elif state == "SCORE" and event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
#                     state = "MENU"
#
#             elif state == "PLAYING" and event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     state = "PAUSED"
#                 elif event.key == pygame.K_SPACE:
#                     b = Bullet(game.player.rect.centerx, game.player.rect.top)
#                     game.bullets.add(b)
#                     game.all_sprites.add(b)
#
#             elif state == "PAUSED" and event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     state = "PLAYING"
#
#         if state == "MENU":
#             menu_background.draw(screen)
#             title_text = "Zombie Shoot"
#             title_rect = title_font.render(title_text, True, (255, 0, 0)).get_rect(center=(SCREEN_WIDTH // 2, 140))
#             draw_shadow_text(screen, title_text, title_font, (255, 0, 0), (title_rect.x, title_rect.y))
#             for i, option in enumerate(options):
#                 color = (255, 0, 0) if i == selected_index else WHITE
#                 rect = font.render(option, True, color).get_rect(center=(SCREEN_WIDTH // 2, 425 + i * 60))
#                 draw_outlined_text(screen, option, font, color, (rect.x, rect.y))
#
#         elif state == "OPTIONS":
#             options_background.draw(screen)
#             draw_outlined_text(screen, "Controles", font, WHITE, (860, 200))
#             draw_outlined_text(screen, "Tecla de Espaço: Atira", small_font, WHITE, (800, 350))
#             draw_outlined_text(screen, "Setas do teclado: Movimentação", small_font, WHITE, (800, 400))
#             draw_outlined_text(screen, "Tecla ESC: Pause", small_font, WHITE, (800, 450))
#             draw_outlined_text(screen, "Pressione ENTER para voltar", small_font, (255, 255, 0), (800, 550))
#
#         elif state == "SCORE":
#             score_background.draw(screen)
#             draw_outlined_text(screen, "Ranking", score_title_font, WHITE, (60, 80))
#             draw_outlined_text(screen, "Pos   Name           Score       Date             Hour", score_list_font, YELLOW, (60, 220))
#             for i, row in enumerate(top_scores):
#                 player_name, score, played_date, played_time = row
#                 line = f"{i + 1:2d}      {player_name:<10} {score:5d}    {played_date}    {played_time}"
#                 draw_outlined_text(screen, line, score_list_font, WHITE, (60, 260 + i * 36))
#             draw_outlined_text(screen, "Pressione ENTER ou ESC para voltar", small_font, (255, 255, 0), (60, 650))
#
#         elif state == "PLAYING":
#             game.update(keys)
#             game.draw()
#             if not end_popup_active and (getattr(game, 'defeated', False) or getattr(game, 'victory', False)):
#                 end_popup_active = True
#                 if game.victory:
#                     end_result_text = "VITORIA"
#                 else:
#                     end_result_text = "DERROTA"
#                 player_name_input = ""
#                 score_saved = False
#
#             if end_popup_active:
#                 overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
#                 overlay.set_alpha(200)
#                 overlay.fill((0, 0, 0))
#                 screen.blit(overlay, (0, 0))
#                 result_rect = popup_font.render(end_result_text, True, WHITE).get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120))
#                 draw_outlined_text(screen, end_result_text, popup_font, WHITE, (result_rect.x, result_rect.y))
#                 score_text = f"Score: {game.score}"
#                 score_rect = popup_font.render(score_text, True, YELLOW).get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
#                 draw_outlined_text(screen, score_text, popup_font, YELLOW, (score_rect.x, score_rect.y))
#                 prompt_text = "Digite seu nome (max 10):"
#                 prompt_rect = input_font.render(prompt_text, True, WHITE).get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
#                 draw_outlined_text(screen, prompt_text, input_font, WHITE, (prompt_rect.x, prompt_rect.y))
#                 input_text = player_name_input if player_name_input else "_"
#                 input_rect = input_font.render(input_text, True, WHITE).get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
#                 draw_outlined_text(screen, input_text, input_font, WHITE, (input_rect.x, input_rect.y))
#                 confirm_text = "ENTER salva | BACKSPACE apaga"
#                 confirm_rect = small_font.render(confirm_text, True, (255, 255, 0)).get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
#                 draw_outlined_text(screen, confirm_text, small_font, (255, 255, 0), (confirm_rect.x, confirm_rect.y))
#                 cancel_text = "Caso não queira salvar, aperte ESC"
#                 cancel_rect = small_font.render(cancel_text, True, (255, 255, 0)).get_rect(
#                     center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200))
#                 draw_outlined_text(screen, cancel_text, small_font, (255, 255, 0), (cancel_rect.x, cancel_rect.y))
#
#         elif state == "PAUSED":
#             game.draw()
#             paused_text = "PAUSADO"
#             paused_rect = pause_font.render(paused_text, True, WHITE).get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
#             draw_outlined_text(screen, paused_text, pause_font, WHITE, (paused_rect.x, paused_rect.y))
#             continue_text = "Pressione ESC para continuar"
#             continue_rect = small_font.render(continue_text, True, (255, 255, 0)).get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
#             draw_outlined_text(screen, continue_text, small_font, (255, 255, 0), (continue_rect.x, continue_rect.y))
#
#         pygame.display.flip()
#         clock.tick(FPS)
#
#     pygame.quit()
#
#
# if __name__ == "__main__":
#     main()



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


def draw_shadow_text(screen, text, font, color, pos, shadow_offset=(10, 10)):
    shadow = font.render(text, True, (30, 30, 30))
    outline = font.render(text, True, (0, 0, 0))
    rendered = font.render(text, True, color)
    screen.blit(shadow, (pos[0] + shadow_offset[0], pos[1] + shadow_offset[1]))
    screen.blit(outline, (pos[0] - 2, pos[1] - 2))
    screen.blit(rendered, pos)


def init_score_db():
    conn = sqlite3.connect(SCORE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            score INTEGER NOT NULL,
            played_date TEXT NOT NULL,
            played_time TEXT NOT NULL,
            played_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_score(player_name, score):
    now = datetime.datetime.now()
    played_date = now.strftime("%d/%m/%Y")
    played_time = now.strftime("%H:%M:%S")
    played_at = now.isoformat()
    conn = sqlite3.connect(SCORE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO scores (player_name, score, played_date, played_time, played_at)
        VALUES (?, ?, ?, ?, ?)
    """, (player_name.strip().upper(), score, played_date, played_time, played_at))
    conn.commit()
    conn.close()


def get_top_scores(limit=10):
    conn = sqlite3.connect(SCORE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT player_name, score, played_date, played_time
        FROM scores
        ORDER BY score DESC, played_at DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Menu")
    menu_background = Background(MENU_PATH)
    options_background = Background(OPTIONS_PATH)
    score_background = Background(SCORE_PATH)
    clock = pygame.time.Clock()
    pygame.mixer.init()
    current_music = None

    init_score_db()

    running = True
    state = "MENU"
    game = None

    options = ["Start", "Options", "Score", "Exit"]
    selected_index = 0
    font = pygame.font.SysFont("28 Days Later", 70, bold=False)
    small_font = pygame.font.SysFont("Arial", 40, bold=False)
    pause_font = pygame.font.SysFont("28 Days Later", 80, bold=False)
    title_font = pygame.font.SysFont("28 Days Later", 145, bold=False)
    popup_font = pygame.font.SysFont("28 Days Later", 60, bold=False)
    input_font = pygame.font.SysFont("Arial", 50, bold=False)
    score_title_font = pygame.font.SysFont("28 Days Later", 80, bold=False)
    score_list_font = pygame.font.SysFont("Arial", 32, bold=False)

    end_popup_active = False
    player_name_input = ""
    end_result_text = ""
    score_saved = False
    top_scores = []

    while running:
        keys = pygame.key.get_pressed()
        if state in ["MENU", "OPTIONS", "SCORE"]:
            if current_music != "MENU":
                play_music(MENU_MUSIC_PATH)
                current_music = "MENU"
        elif state in ["PLAYING", "PAUSED"]:
            if current_music != "GAME":
                play_music(GAME_MUSIC_PATH)
                current_music = "GAME"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if end_popup_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if player_name_input.strip():
                            save_score(player_name_input.strip().upper(), game.score)
                            score_saved = True
                            end_popup_active = False
                            player_name_input = ""
                            end_result_text = ""
                            state = "MENU"
                            game = None
                    elif event.key == pygame.K_ESCAPE:
                        end_popup_active = False
                        player_name_input = ""
                        end_result_text = ""
                        score_saved = False
                        state = "MENU"
                        game = None
                    elif event.key == pygame.K_BACKSPACE:
                        player_name_input = player_name_input[:-1]
                    elif event.unicode.isalnum():
                        if len(player_name_input) < 10:
                            player_name_input += event.unicode.upper()
                continue

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
                    elif choice == "Score":
                        state = "SCORE"
                        top_scores = get_top_scores(10)
                    elif choice == "Exit":
                        running = False

            elif state == "OPTIONS" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    state = "MENU"

            elif state == "SCORE" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    state = "MENU"

            elif state == "PLAYING" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "PAUSED"
                elif event.key == pygame.K_SPACE:
                    b = Bullet(game.player.rect.centerx, game.player.rect.top)
                    game.bullets.add(b)
                    game.all_sprites.add(b)

            elif state == "PAUSED" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "PLAYING"

        if state == "MENU":
            menu_background.draw(screen)
            title_text = "Zombie Shoot"
            title_rect = title_font.render(title_text, True, (255, 0, 0)).get_rect(center=(SCREEN_WIDTH // 2, 140))
            draw_shadow_text(screen, title_text, title_font, (255, 0, 0), (title_rect.x, title_rect.y))
            for i, option in enumerate(options):
                color = (255, 0, 0) if i == selected_index else WHITE
                rect = font.render(option, True, color).get_rect(center=(SCREEN_WIDTH // 2, 425 + i * 60))
                draw_outlined_text(screen, option, font, color, (rect.x, rect.y))

        elif state == "OPTIONS":
            options_background.draw(screen)
            draw_outlined_text(screen, "Controles", font, WHITE, (860, 200))
            draw_outlined_text(screen, "Tecla de Espaço: Atira", small_font, WHITE, (800, 350))
            draw_outlined_text(screen, "Setas do teclado: Movimentação", small_font, WHITE, (800, 400))
            draw_outlined_text(screen, "Tecla ESC: Pause", small_font, WHITE, (800, 450))
            draw_outlined_text(screen, "Pressione ENTER para voltar", small_font, (255, 255, 0), (800, 550))

        elif state == "SCORE":
            score_background.draw(screen)
            draw_outlined_text(screen, "Ranking", score_title_font, WHITE, (60, 80))
            draw_outlined_text(screen, "Pos   Name           Score       Date             Hour", score_list_font, YELLOW, (60, 220))
            for i, row in enumerate(top_scores):
                player_name, score, played_date, played_time = row
                line = f"{i + 1:2d}      {player_name:<10} {score:5d}    {played_date}    {played_time}"
                draw_outlined_text(screen, line, score_list_font, WHITE, (60, 260 + i * 36))
            draw_outlined_text(screen, "Pressione ENTER ou ESC para voltar", small_font, (255, 255, 0), (60, 650))

        elif state == "PLAYING":
            game.update(keys)
            game.draw()
            if not end_popup_active and (getattr(game, 'defeated', False) or getattr(game, 'victory', False)):
                end_popup_active = True
                if game.victory:
                    end_result_text = "VITORIA"
                else:
                    end_result_text = "DERROTA"
                player_name_input = ""
                score_saved = False

            if end_popup_active:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.set_alpha(200)
                overlay.fill((0, 0, 0))
                screen.blit(overlay, (0, 0))
                result_rect = popup_font.render(end_result_text, True, WHITE).get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120))
                draw_outlined_text(screen, end_result_text, popup_font, WHITE, (result_rect.x, result_rect.y))
                score_text = f"Score: {game.score}"
                score_rect = input_font.render(score_text, True, YELLOW).get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
                draw_outlined_text(screen, score_text, input_font, YELLOW, (score_rect.x, score_rect.y))
                prompt_text = "Digite seu nome (max 10):"
                prompt_rect = input_font.render(prompt_text, True, WHITE).get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
                draw_outlined_text(screen, prompt_text, input_font, WHITE, (prompt_rect.x, prompt_rect.y))
                input_text = player_name_input if player_name_input else "_"
                input_rect = input_font.render(input_text, True, WHITE).get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
                draw_outlined_text(screen, input_text, input_font, WHITE, (input_rect.x, input_rect.y))
                confirm_text = "ENTER salva | BACKSPACE apaga"
                confirm_rect = small_font.render(confirm_text, True, (255, 255, 0)).get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
                draw_outlined_text(screen, confirm_text, small_font, (255, 255, 0), (confirm_rect.x, confirm_rect.y))
                cancel_text = "Caso não queira salvar, aperte ESC"
                cancel_rect = small_font.render(cancel_text, True, (255, 255, 0)).get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200))
                draw_outlined_text(screen, cancel_text, small_font, (255, 255, 0), (cancel_rect.x, cancel_rect.y))

        elif state == "PAUSED":
            game.draw()
            paused_text = "PAUSADO"
            paused_rect = pause_font.render(paused_text, True, WHITE).get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
            draw_outlined_text(screen, paused_text, pause_font, WHITE, (paused_rect.x, paused_rect.y))
            continue_text = "Pressione ESC para continuar"
            continue_rect = small_font.render(continue_text, True, (255, 255, 0)).get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            draw_outlined_text(screen, continue_text, small_font, (255, 255, 0), (continue_rect.x, continue_rect.y))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()