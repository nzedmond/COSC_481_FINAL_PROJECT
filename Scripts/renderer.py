from pyray import *
from constants import *

def get_terrain_variant(level, row, col):
    "Determine which terrain tile variant to use based on neighboring tiles"
    from level import TILE_ROWS, TILE_COLS
    
    def is_solid(r, c):
        if r < 0 or r >= TILE_ROWS or c < 0 or c >= TILE_COLS:
            return False
        return level[r][c] == TILE_SOLID
    
    above = is_solid(row - 1, col)
    below = is_solid(row + 1, col)
    left = is_solid(row, col - 1)
    right = is_solid(row, col + 1)
    
    if not above and not left:
        return "top_left"
    elif not above and not right:
        return "top_right"
    elif not above:
        return "top"
    elif not left and not below:
        return "bottom_left"
    elif not right and not below:
        return "bottom_right"
    elif not below:
        return "bottom"
    elif not left:
        return "left"
    elif not right:
        return "right"
    else:
        return "center"

def draw_tiled_background(bg_texture, world_width, world_height):
    """Tile the background image across the entire world."""
    x = 0
    while x < world_width:
        y = 0
        while y < world_height:
            draw_texture(bg_texture, x, y, WHITE)
            y += bg_texture.height
        x += bg_texture.width

def draw_level(level, terrain_texture=None):
    """Draws the solid tiles using the terrain spritesheet, or fallback rects."""
    from level import TILE_ROWS, TILE_COLS

    for row in range(TILE_ROWS):
        for col in range(TILE_COLS):
            if level[row][col] == TILE_SOLID:
                x = col * TILE_SIZE
                y = row * TILE_SIZE

                if terrain_texture is not None:
                    variant = get_terrain_variant(level, row, col)
                    tc, tr = TERRAIN_TILES[variant]
                    source = Rectangle(
                        tc * TERRAIN_TILE_SIZE,
                        tr * TERRAIN_TILE_SIZE,
                        TERRAIN_TILE_SIZE,
                        TERRAIN_TILE_SIZE
                    )
                    dest = Rectangle(x, y, TILE_SIZE, TILE_SIZE)
                    draw_texture_pro(terrain_texture, source, dest,
                                     Vector2(0, 0), 0.0, WHITE)
                else:
                    draw_rectangle(x, y, TILE_SIZE, TILE_SIZE, DARKGRAY)
                    draw_rectangle_lines(x, y, TILE_SIZE, TILE_SIZE, BLACK)

COIN_FRAME_COUNT = 6

def draw_coins(coins, coin_sheet, coin_frame):
    """Draws the active coins using the rotate spritesheet."""
    frame_width = coin_sheet.width // COIN_FRAME_COUNT + 40
    frame_height = coin_sheet.height
    size = TILE_SIZE * 0.9

    source = Rectangle(coin_frame * frame_width, 0, frame_width-30, frame_height)
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
