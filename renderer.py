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


COIN_FRAME_COUNT = 6

def draw_coins(coins, coin_sheet, coin_frame):
    """Draws the active coins using the rotate spritesheet."""
    frame_width = coin_sheet.width // COIN_FRAME_COUNT
    frame_height = coin_sheet.height
    size = TILE_SIZE * 0.9

    source = Rectangle(coin_frame * frame_width, 0, frame_width, frame_height)
    for cx, cy in coins:
        dest = Rectangle(cx - size / 2, cy - size / 2, size, size)
        draw_texture_pro(coin_sheet, source, dest, Vector2(0, 0), 0.0, WHITE)


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
