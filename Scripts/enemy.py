from pyray import *
from constants import *
import math

BULLET_SPEED  = 380.0   # pixels / second
BULLET_RADIUS = 5


class Bullet:
    def __init__(self, wx, wy, target_x, target_y):
        self.x = float(wx)
        self.y = float(wy)

        dx = target_x - wx
        dy = target_y - wy
        dist = math.hypot(dx, dy) or 1.0
        self.vx = dx / dist * BULLET_SPEED
        self.vy = dy / dist * BULLET_SPEED
        self.active = True

    # ------------------------------------------------------------------
    def update(self, dt, level):
        if not self.active:
            return

        self.x += self.vx * dt
        self.y += self.vy * dt

        # Tile collision — bullet disappears when it hits a solid tile
        from level import TILE_ROWS, TILE_COLS
        col = int(self.x / TILE_SIZE)
        row = int(self.y / TILE_SIZE)
        if 0 <= row < TILE_ROWS and 0 <= col < TILE_COLS:
            if level[row][col] == TILE_SOLID:
                self.active = False
                return

        # Out of world bounds
        from level import WORLD_WIDTH, WORLD_HEIGHT
        if self.x < 0 or self.x > WORLD_WIDTH or self.y < 0 or self.y > WORLD_HEIGHT:
            self.active = False

    # ------------------------------------------------------------------
    def draw(self):
        if not self.active:
            return
        cx, cy = int(self.x), int(self.y)
        draw_circle(cx, cy, BULLET_RADIUS,     RED)
        draw_circle(cx, cy, BULLET_RADIUS - 2, ORANGE)

    # ------------------------------------------------------------------
    def get_rect(self):
        r = BULLET_RADIUS
        return (self.x - r, self.y - r, r * 2, r * 2)
