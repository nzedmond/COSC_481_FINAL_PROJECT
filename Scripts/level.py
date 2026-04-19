from constants import *

# ---------------------------------------------------------------------------
# Cemetery level — 16 rows × 50 columns, TILE_SIZE = 40 px
#
# Legend:
#   0 = air
#   1 = solid tile
#   2 = coin  (extracted by parse_level, replaced with air)
#   3 = enemy (extracted by parse_level, replaced with air)
#
# Platform heights (world-y = row × 40):
#   row  3 → y=120  (highest)
#   row  5 → y=200
#   row  7 → y=280
#   row  9 → y=360
#   row 11 → y=440
#   row 13 → y=520
#   row 14 → y=560  (enemy patrol row, just above ground)
#   row 15 → y=600  (solid ground)
# ---------------------------------------------------------------------------

LEVEL = [
    # col  0         1         2         3         4
    #      0123456789012345678901234567890123456789012345678 9
    # 0 — open sky
    [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0],
    # 1
    [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0],
    # 2
    [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0],
    # 3 — highest platforms + coin
    [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,2,0,1,1,1,1,0],
    # 4
    [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0],
    # 5 — high platforms
    [0,0,0,0,0,1,1,1,1,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,1,1,1,1,0, 0,0,0,0,0,0,0,0,0,0],
    # 6 — coins above high platforms
    [0,0,2,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,2,0,0,0,0,0,0,0,0],
    # 7 — mid-high platforms
    [0,0,0,0,0,0,0,0,0,0, 0,1,1,1,1,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,1,1,1,1,0,0,0],
    # 8 — coins
    [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,2,0,0, 0,0,0,0,0,0,0,0,0,0, 0,2,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0],
    # 9 — mid platforms
    [0,0,0,1,1,1,1,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,1,1,1,1,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,1,1,1],
    # 10 — enemies in the second half only (col 25+)
    [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,3,0, 0,0,0,2,0,0,0,0,0,0, 0,0,3,0,0,0,0,0,0,0],
    # 11 — lower-mid platforms
    [0,0,0,0,0,0,0,0,0,0, 0,0,1,1,1,1,1,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,1,1,1,1,0, 0,0,0,0,0,0,0,0,0,0],
    # 12 — coins
    [0,2,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,2,0, 0,0,0,0,0,0,0,0,0,0, 0,2,0,0,0,0,0,0,0,0, 0,0,0,0,2,0,0,0,0,0],
    # 13 — low platforms
    [0,0,0,0,1,1,1,1,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,1,1,1,1,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,1,1,1,1],
    # 14 — enemy patrol row just above ground, second half only (col 25+)
    [0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,3, 0,0,0,0,3,0,0,0,0,0, 0,0,0,0,0,0,0,3,0,0],
    # 15 — solid ground
    [1,1,1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1,1,1],
]

TILE_ROWS = len(LEVEL)
TILE_COLS = len(LEVEL[0])
WORLD_WIDTH  = TILE_COLS * TILE_SIZE
WORLD_HEIGHT = TILE_ROWS * TILE_SIZE


def parse_level(level):
    """Extract coins and enemies from the tilemap, return the clean collision
    map plus lists of entity spawn positions / objects."""
    from enemy import Enemy

    coins   = []
    enemies = []
    new_level = [row[:] for row in level]

    for r in range(TILE_ROWS):
        for c in range(TILE_COLS):
            x = c * TILE_SIZE
            y = r * TILE_SIZE

            if new_level[r][c] == TILE_COIN:
                coins.append((x + TILE_SIZE / 2, y + TILE_SIZE / 2))
                new_level[r][c] = TILE_AIR

            elif new_level[r][c] == TILE_ENEMY:
                enemies.append(Enemy(x, y))
                new_level[r][c] = TILE_AIR

    return new_level, coins, enemies
