import sqlite3
import datetime
import pygame
from code.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, MENU_PATH, MENU_MUSIC_PATH, GAME_MUSIC_PATH, SCORE_PATH, \
    OPTIONS_PATH, SCORE_DB_PATH, YELLOW
from code.background import Background
from code.entities import Bullet
from code.game import Game

def play_music(path):
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)
    except Exception:
        pass

def draw_outlined_text(screen, text, font, color, pos):
    outline = font.render(text, True, (0, 0, 0))
    rendered = font.render(text, True, color)
    screen.blit(outline, (pos[0] - 3, pos[1] - 3))
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
    pause_font = pygame.font.SysFont("28 Days Later", 90, bold=False)
    title_font = pygame.font.SysFont("28 Days Later", 145, bold=False)
    popup_font = pygame.font.SysFont("28 Days Later", 60, bold=False)
    input_font = pygame.font.SysFont("Arial", 50, bold=False)
    score_title_font = pygame.font.SysFont("28 Days Later", 100, bold=False)
    score_list_font = pygame.font.SysFont("Arial", 32, bold=False)

    end_popup_active = False
    player_name_input = ""
    end_result_text = ""
    score_saved = False
    top_scores = []
    game_over_wait_start = 0

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
                if game_over_wait_start != 0:
                    continue
                if event.key == pygame.K_ESCAPE:
                    state = "PAUSED"
                elif event.key == pygame.K_SPACE:
                    if game.is_rapid_fire_active():
                        bullets = [
                            Bullet(game.player.rect.centerx - 15, game.player.rect.top),
                            Bullet(game.player.rect.centerx + 15, game.player.rect.top)
                        ]
                        for b in bullets:
                            game.bullets.add(b)
                            game.all_sprites.add(b)
                    else:
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
            draw_outlined_text(screen, "Controles", pause_font, WHITE, (840, 200))
            draw_outlined_text(screen, "Tecla de Espaço: Atira", small_font, WHITE, (800, 350))
            draw_outlined_text(screen, "Setas do teclado: Movimentação", small_font, WHITE, (800, 400))
            draw_outlined_text(screen, "Tecla ESC: Pause", small_font, WHITE, (800, 450))
            draw_outlined_text(screen, "Pressione ENTER para voltar", small_font, (255, 255, 0), (800, 550))

        elif state == "SCORE":

            score_background.draw(screen)
            draw_outlined_text(screen, "Ranking", score_title_font, WHITE, (770, 80))

            rank_x = 640
            name_x = 710
            score_x = 870
            date_x = 990
            hour_x = 1150
            row_y = 220
            row_height = 36

            draw_outlined_text(screen, "Pos", score_list_font, YELLOW, (rank_x, row_y))
            draw_outlined_text(screen, "Name", score_list_font, YELLOW, (name_x, row_y))
            draw_outlined_text(screen, "Score", score_list_font, YELLOW, (score_x, row_y))
            draw_outlined_text(screen, "Date", score_list_font, YELLOW, (date_x, row_y))
            draw_outlined_text(screen, "Hour", score_list_font, YELLOW, (hour_x, row_y))

            for i, row in enumerate(top_scores):
                player_name, score, played_date, played_time = row

                ordinal = f"{i + 1}º"

                y = row_y + row_height + i * row_height

                draw_outlined_text(screen, ordinal, score_list_font, WHITE, (rank_x, y))
                draw_outlined_text(screen, player_name, score_list_font, WHITE, (name_x, y))
                draw_outlined_text(screen, str(score), score_list_font, WHITE, (score_x, y))
                draw_outlined_text(screen, played_date, score_list_font, WHITE, (date_x, y))
                draw_outlined_text(screen, played_time, score_list_font, WHITE, (hour_x, y))
                draw_outlined_text(screen, "Pressione ENTER ou ESC para voltar", small_font, (255, 255, 0), (670, 700))

        elif state == "PLAYING":
            game.update(keys)
            game.draw()

            if not end_popup_active and game_over_wait_start == 0 and (
                    getattr(game, 'defeated', False) or getattr(game, 'victory', False)):
                game_over_wait_start = pygame.time.get_ticks()
                if game.victory:
                    end_result_text = "VITORIA"
                else:
                    end_result_text = "DERROTA"
                player_name_input = ""
                score_saved = False

            if game_over_wait_start != 0 and not end_popup_active:
                if pygame.time.get_ticks() - game_over_wait_start >= 2000:
                    end_popup_active = True
                    game_over_wait_start = 0

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
























