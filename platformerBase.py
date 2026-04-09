from raylib import *
from pyray import *
from constants import *
from level import parse_level, LEVEL, WORLD_WIDTH, WORLD_HEIGHT
from player import Player
from renderer import draw_level, draw_coins, update_camera
from game_state import GameState


def main():
    InitWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "Raylib 2D Platformer Clone (Stomp Mechanic)".encode('utf-8'))
    SetTargetFPS(60)

    game_level, collectibles, enemies = parse_level(LEVEL)

    coin_sheet = load_texture("coins/rotate.png".encode())
    coin_frame = 0
    anim_timer = 0.0

    player = Player(TILE_SIZE * 2, TILE_SIZE * 2)
    score = 0
    game_state = GameState.MENU

    camera = Camera2D()
    camera.target = Vector2(player.x, player.y)
    camera.offset = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    camera.rotation = 0.0
    camera.zoom = 1.0

    while not WindowShouldClose():
        delta_time = GetFrameTime()

        # --- Update ---
        anim_timer += delta_time
        if anim_timer >= 0.1:
            anim_timer = 0.0
            coin_frame = (coin_frame + 1) % 6

        if game_state == GameState.MENU:
            if IsKeyPressed(KEY_ENTER):
                game_state = GameState.PLAYING

        elif game_state == GameState.PLAYING:
            if IsKeyPressed(KEY_P):
                game_state = GameState.PAUSED

            player.update(delta_time, game_level)

            for enemy in enemies:
                enemy.update(delta_time, game_level)

            update_camera(camera, player, WORLD_WIDTH, WORLD_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT)

            collected_indices = player.check_collection(collectibles)
            if collected_indices:
                for index in sorted(collected_indices, reverse=True):
                    collectibles.pop(index)
                    score += 10

            if len(collectibles) == 0:
                game_state = GameState.WIN

            hit_type, enemy_index = player.check_enemy_collision(enemies)

            if hit_type == "STOMP":
                enemies.pop(enemy_index)
                score += 100
                player.vy = STOMP_BOUNCE

            elif hit_type == "LETHAL":
                player.reset()
                score -= 50
                if score < 0:
                    score = 0

        elif game_state == GameState.PAUSED:
            if IsKeyPressed(KEY_P):
                game_state = GameState.PLAYING

        # --- Draw ---
        BeginDrawing()
        ClearBackground(SKYBLUE)

        BeginMode2D(camera)
        draw_level(game_level)
        draw_coins(collectibles, coin_sheet, coin_frame)
        for enemy in enemies:
            enemy.draw()
        player.draw()
        EndMode2D()

        score_text = f"Score: {score}".encode('utf-8')
        DrawText(score_text, SCREEN_WIDTH - MeasureText(score_text, 20) - 10, 10, 20, BLACK)

        debug_text = f"Grounded: {player.is_grounded} | Enemies: {len(enemies)}".encode('utf-8')
        DrawText(debug_text, 10, 10, 20, BLACK)

        if game_state == GameState.MENU:
            menu_text = "Press ENTER to Play".encode('utf-8')
            DrawText(menu_text, SCREEN_WIDTH // 2 - MeasureText(menu_text, 30) // 2, SCREEN_HEIGHT // 2 - 15, 30, WHITE)

        elif game_state == GameState.PAUSED:
            pause_text = "PAUSED".encode('utf-8')
            DrawText(pause_text, SCREEN_WIDTH // 2 - MeasureText(pause_text, 40) // 2, SCREEN_HEIGHT // 2 - 20, 40, WHITE)
            resume_text = "Press P to Resume".encode('utf-8')
            DrawText(resume_text, SCREEN_WIDTH // 2 - MeasureText(resume_text, 20) // 2, SCREEN_HEIGHT // 2 + 30, 20, LIGHTGRAY)

        elif game_state == GameState.WIN:
            win_text = "You won!".encode('utf-8')
            DrawText(win_text, SCREEN_WIDTH // 2 - MeasureText(win_text, 40) // 2, SCREEN_HEIGHT // 2 - 20, 40, GREEN)
            final_text = f"Final score: {score}".encode('utf-8')
            DrawText(final_text, SCREEN_WIDTH // 2 - MeasureText(final_text, 20) // 2, SCREEN_HEIGHT // 2 + 30, 20, BLACK)

        EndDrawing()

    unload_texture(coin_sheet)
    CloseWindow()


if __name__ == "__main__":
    main()
