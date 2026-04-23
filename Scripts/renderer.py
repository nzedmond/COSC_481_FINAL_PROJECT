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


def draw_level(level, terrain_texture=None, variant='cemetery'):
    """Draw solid tiles using the given tileset variant, or fallback rectangles.

    variant: 'cemetery' uses the grass-stone cemetery sheet;
             'church'   uses the gray-stone inside-church sheet.
    """
    from level import TILE_ROWS, TILE_COLS

    if variant == 'church':
        surface_src = (CHURCH_SURFACE_X, CHURCH_SURFACE_Y, CHURCH_SURFACE_W, CHURCH_SURFACE_H)
        fill_src    = (CHURCH_FILL_X,    CHURCH_FILL_Y,    CHURCH_FILL_W,    CHURCH_FILL_H)
    else:
        surface_src = (CEMETERY_SURFACE_X, CEMETERY_SURFACE_Y, CEMETERY_SURFACE_W, CEMETERY_SURFACE_H)
        fill_src    = (CEMETERY_FILL_X,    CEMETERY_FILL_Y,    CEMETERY_FILL_W,    CEMETERY_FILL_H)

    for row in range(TILE_ROWS):
        for col in range(TILE_COLS):
            if level[row][col] != TILE_SOLID:
                continue

            x = col * TILE_SIZE
            y = row * TILE_SIZE

            if terrain_texture is not None and terrain_texture.id > 0:
                is_surface = (row == 0 or level[row - 1][col] != TILE_SOLID)
                sx, sy, sw, sh = surface_src if is_surface else fill_src
                src  = Rectangle(sx, sy, sw, sh)
                dest = Rectangle(x, y, TILE_SIZE, TILE_SIZE)
                draw_texture_pro(terrain_texture, src, dest, Vector2(0, 0), 0.0, WHITE)
            else:
                draw_rectangle(x, y, TILE_SIZE, TILE_SIZE, DARKGRAY)
                draw_rectangle_lines(x, y, TILE_SIZE, TILE_SIZE, BLACK)


COIN_FRAME_COUNT = 17  # Apple.png spritesheet: 544x32, 17 frames of 32x32


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
