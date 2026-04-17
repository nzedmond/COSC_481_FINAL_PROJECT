# --- Screen ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# --- Tile ---
TILE_SIZE = 40

# --- Physics ---
GRAVITY = 1800.0
JUMP_VELOCITY = -750.0
STOMP_BOUNCE = JUMP_VELOCITY * 0.6

# --- Movement ---
PLAYER_SPEED = 300.0
ENEMY_SPEED = 100.0

# --- Player Size ---
PLAYER_WIDTH = TILE_SIZE * 0.8
PLAYER_HEIGHT = TILE_SIZE * 0.9

# --- Tile Types ---
TILE_AIR = 0
TILE_SOLID = 1
TILE_COIN = 2
TILE_ENEMY = 3

# ---- Terrain Spritesheet --------

TERRAIN_TILE_SIZE = 16
TERRAIN_TILES = {
    "top_left": (0, 0),
    "top": (1, 0),
    "top_right": (2, 0),
    "left": (0, 1),
    "center": (1, 1),
    "right": (2, 1),
    "bottom_left": (0, 2),
    "bottom": (1, 2),
    "bottom_right": (2, 2),
}
