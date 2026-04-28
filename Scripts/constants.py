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

# --- Win condition ---
# Column index of the finish zone (right end of the 50-col level)
DEST_COL = 47

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

# --- Inside Church Tileset source rects within Terrain (16x16).png (352x176) ---
# Gray stone interior fill tile (col 1, row 1 of the stone pack)
CHURCH_FILL_X = 16
CHURCH_FILL_Y = 16
CHURCH_FILL_W = 16
CHURCH_FILL_H = 16

# Gray stone surface tile — slightly lighter top (col 1, row 0 of the stone pack)
CHURCH_SURFACE_X = 16
CHURCH_SURFACE_Y = 0
CHURCH_SURFACE_W = 16
CHURCH_SURFACE_H = 16

# --- Level 1 tileset — col 2 (x=32) of Terrain (16x16).png ---
L1_SURFACE_X = 32
L1_SURFACE_Y = 0
L1_SURFACE_W = 16
L1_SURFACE_H = 16

L1_FILL_X = 32
L1_FILL_Y = 16
L1_FILL_W = 16
L1_FILL_H = 16
