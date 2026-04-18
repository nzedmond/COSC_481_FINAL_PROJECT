from pyray import *
from constants import *
from level import parse_level, LEVEL, WORLD_WIDTH, WORLD_HEIGHT
from player import Player
from renderer import draw_level, draw_coins, update_camera, draw_parallax_layer
from game_state import GameState


def main():
    init_window(SCREEN_WIDTH, SCREEN_HEIGHT, b"Crossing Kabgayi - The Broken Sanctuary")
    set_target_fps(60)

    game_level, collectibles, enemies = parse_level(LEVEL)

    # --- Load cemetery background layers (far → near) ---
    bg0_tex       = load_texture(b"Assets/cemetery/Background_0.png")       # night sky
    bg1_tex       = load_texture(b"Assets/cemetery/Background_1.png")       # buildings
    grass_bg1_tex = load_texture(b"Assets/cemetery/Grass_background_1.png") # gravestones
    grass_bg2_tex = load_texture(b"Assets/cemetery/Grass_background_2.png") # dead tree

    # --- Load cemetery tile texture and coin animation ---
    tiles_tex  = load_texture(b"Assets/cemetery/Tiles.png")
    coin_sheet = load_texture(b"coins/rotate.png")
    coin_frame = 0
    anim_timer = 0.0

    # Spawn player just above the ground on the left side
    player = Player(TILE_SIZE * 2, TILE_SIZE * 14)
    score = 0
    game_state = GameState.MENU

    camera = Camera2D()
    camera.target = Vector2(player.x, player.y)
    camera.offset = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    camera.rotation = 0.0
    camera.zoom = 1.0

    while not window_should_close():
        delta_time = get_frame_time()

        # --- Update ---
        anim_timer += delta_time
        if anim_timer >= 0.1:
            anim_timer = 0.0
            coin_frame = (coin_frame + 1) % 6

        if game_state == GameState.MENU:
            if is_key_pressed(KEY_ENTER):
                game_state = GameState.PLAYING

        elif game_state == GameState.PLAYING:
            if is_key_pressed(KEY_P):
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
            if is_key_pressed(KEY_P):
                game_state = GameState.PLAYING

        # --- Draw ---
        begin_drawing()
        clear_background(BLACK)

        # Parallax backgrounds drawn in screen space (before world geometry).
        # Each layer scrolls at a fraction of the camera speed — smaller
        # factor = farther away = moves less.
        draw_parallax_layer(bg0_tex,       camera.target.x, 0.05, SCREEN_WIDTH, SCREEN_HEIGHT)
        draw_parallax_layer(bg1_tex,       camera.target.x, 0.15, SCREEN_WIDTH, SCREEN_HEIGHT)
        draw_parallax_layer(grass_bg1_tex, camera.target.x, 0.30, SCREEN_WIDTH, SCREEN_HEIGHT)
        draw_parallax_layer(grass_bg2_tex, camera.target.x, 0.50, SCREEN_WIDTH, SCREEN_HEIGHT)

        # World-space geometry drawn on top of the backgrounds.
        begin_mode_2d(camera)
        draw_level(game_level, tiles_tex)
        draw_coins(collectibles, coin_sheet, coin_frame)
        for enemy in enemies:
            enemy.draw()
        player.draw()
        end_mode_2d()

        # HUD (screen space, white text for dark background)
        score_text = f"Score: {score}".encode('utf-8')
        draw_text(score_text, SCREEN_WIDTH - measure_text(score_text, 20) - 10, 10, 20, WHITE)

        debug_text = f"Grounded: {player.is_grounded} | Enemies: {len(enemies)}".encode('utf-8')
        draw_text(debug_text, 10, 10, 20, WHITE)

        if game_state == GameState.MENU:
            menu_text = b"Press ENTER to Play"
            draw_text(menu_text, SCREEN_WIDTH // 2 - measure_text(menu_text, 30) // 2,
                      SCREEN_HEIGHT // 2 - 15, 30, WHITE)

        elif game_state == GameState.PAUSED:
            pause_text = b"PAUSED"
            draw_text(pause_text, SCREEN_WIDTH // 2 - measure_text(pause_text, 40) // 2,
                      SCREEN_HEIGHT // 2 - 20, 40, WHITE)
            resume_text = b"Press P to Resume"
            draw_text(resume_text, SCREEN_WIDTH // 2 - measure_text(resume_text, 20) // 2,
                      SCREEN_HEIGHT // 2 + 30, 20, LIGHTGRAY)

        elif game_state == GameState.WIN:
            win_text = b"You Won!"
            draw_text(win_text, SCREEN_WIDTH // 2 - measure_text(win_text, 40) // 2,
                      SCREEN_HEIGHT // 2 - 20, 40, GREEN)
            final_text = f"Final Score: {score}".encode('utf-8')
            draw_text(final_text, SCREEN_WIDTH // 2 - measure_text(final_text, 20) // 2,
                      SCREEN_HEIGHT // 2 + 30, 20, WHITE)

        end_drawing()

    # Cleanup
    unload_texture(bg0_tex)
    unload_texture(bg1_tex)
    unload_texture(grass_bg1_tex)
    unload_texture(grass_bg2_tex)
    unload_texture(tiles_tex)
    unload_texture(coin_sheet)
    close_window()


if __name__ == "__main__":
    main()
