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

# --- Cemetery Tileset source rects within Tiles.png (352x384) ---
# Stone brick face — used for solid interior tiles (center of the cross shape)
CEMETERY_FILL_X = 64
CEMETERY_FILL_Y = 64
CEMETERY_FILL_W = 64
CEMETERY_FILL_H = 64

# Grass-topped stone — used for the exposed top surface of platforms
CEMETERY_SURFACE_X = 192
CEMETERY_SURFACE_Y = 0
CEMETERY_SURFACE_W = 64
CEMETERY_SURFACE_H = 64
