from pyray import *
from constants import *


def draw_parallax_layer(texture, camera_x, scroll_factor, screen_width, screen_height, tint=WHITE):
    """Draw a background texture in screen space with parallax scrolling.

    Each layer moves at scroll_factor * camera_x so farther layers (small
    factor) scroll slower than closer ones (large factor), creating depth.
    """
    if texture.id == 0:
        return

    # Scale the texture to fill the screen height exactly.
    scale = screen_height / texture.height
    scaled_w = texture.width * scale

    # Compute horizontal offset and wrap it so it tiles seamlessly.
    offset_x = -(camera_x * scroll_factor) % scaled_w
    if offset_x > 0:
        offset_x -= scaled_w   # keep the anchor tile just off-screen left

    x = offset_x
    while x < screen_width:
        src = Rectangle(0, 0, texture.width, texture.height)
        dest = Rectangle(x, 0, scaled_w, screen_height)
        draw_texture_pro(texture, src, dest, Vector2(0, 0), 0.0, tint)
        x += scaled_w


def draw_level(level, terrain_texture=None):
    """Draw solid tiles using the cemetery tileset, or fallback rectangles."""
    from level import TILE_ROWS, TILE_COLS

    for row in range(TILE_ROWS):
        for col in range(TILE_COLS):
            if level[row][col] != TILE_SOLID:
                continue

            x = col * TILE_SIZE
            y = row * TILE_SIZE

            if terrain_texture is not None and terrain_texture.id > 0:
                # Exposed top → grass-stone surface tile; buried → brick fill.
                is_surface = (row == 0 or level[row - 1][col] != TILE_SOLID)
                if is_surface:
                    src = Rectangle(CEMETERY_SURFACE_X, CEMETERY_SURFACE_Y,
                                    CEMETERY_SURFACE_W, CEMETERY_SURFACE_H)
                else:
                    src = Rectangle(CEMETERY_FILL_X, CEMETERY_FILL_Y,
                                    CEMETERY_FILL_W, CEMETERY_FILL_H)
                dest = Rectangle(x, y, TILE_SIZE, TILE_SIZE)
                draw_texture_pro(terrain_texture, src, dest, Vector2(0, 0), 0.0, WHITE)
            else:
                draw_rectangle(x, y, TILE_SIZE, TILE_SIZE, DARKGRAY)
                draw_rectangle_lines(x, y, TILE_SIZE, TILE_SIZE, BLACK)


COIN_FRAME_COUNT = 6


def draw_coins(coins, coin_sheet, coin_frame):
    """Draw active coins using the rotate spritesheet."""
    frame_width = coin_sheet.width // COIN_FRAME_COUNT
    frame_height = coin_sheet.height
    size = TILE_SIZE * 0.9

    source = Rectangle(coin_frame * frame_width, 0, frame_width, frame_height)
    for cx, cy in coins:
        dest = Rectangle(cx - size / 2, cy - size / 2, size, size)
        draw_texture_pro(coin_sheet, source, dest, Vector2(0, 0), 0.0, WHITE)


def update_camera(camera, player, world_width, world_height, screen_width, screen_height):
    """Centre the camera on the player and clamp to world bounds."""
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
