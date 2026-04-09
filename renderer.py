from pyray import *
from constants import *


def draw_level(level):
    """Draws the solid tiles of the level map."""
    from level import TILE_ROWS, TILE_COLS
    for row in range(TILE_ROWS):
        for col in range(TILE_COLS):
            if level[row][col] == TILE_SOLID:
                x = col * TILE_SIZE
                y = row * TILE_SIZE
                draw_rectangle(x, y, TILE_SIZE, TILE_SIZE, DARKGRAY)
                draw_rectangle_lines(x, y, TILE_SIZE, TILE_SIZE, BLACK)


def draw_coins(coins):
    """Draws the active coins as small yellow diamonds."""
    radius = TILE_SIZE * 0.3 / 2

    for cx, cy in coins:
        v1 = Vector2(cx, cy - radius * 2)
        v2 = Vector2(cx + radius * 1.5, cy)
        v3 = Vector2(cx, cy + radius * 2)
        v4 = Vector2(cx - radius * 1.5, cy)

        draw_triangle(v1, v2, v4, YELLOW)
        draw_triangle(v2, v3, v4, GOLD)
        draw_line_v(v1, v3, BLACK)
        draw_line_v(v2, v4, BLACK)


def update_camera(camera, player, world_width, world_height, screen_width, screen_height):
    """Centers the camera on the player and clamps to world bounds."""
    camera.target.x = player.x + player.width / 2
    camera.target.y = player.y + player.height / 2

    min_x = screen_width / 2
    max_x = world_width - screen_width / 2
    if camera.target.x < min_x:
        camera.target.x = min_x
    if camera.target.x > max_x:
        camera.target.x = max_x

    min_y = screen_height / 2
    max_y = world_height - screen_height / 2
    if camera.target.y < min_y:
        camera.target.y = min_y
    if camera.target.y > max_y:
        camera.target.y = max_y

    camera.offset.x = screen_width / 2
    camera.offset.y = screen_height / 2
