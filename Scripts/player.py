from pyray import *
from constants import *


class Player:
    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT

        self.jump_count = 0
        self.max_jumps = 2

        # Physics
        self.vx = 0.0
        self.vy = 0.0
        self.is_grounded = False

        # Health — persists between respawns; depletes on enemy hits
        self.max_health = 100
        self.health     = self.max_health

        self.sprites = {
            "idle": load_texture(b"Assets/inside_church/Main Characters/Ninja Frog/Idle (32x32).png"),
            "run":  load_texture(b"Assets/inside_church/Main Characters/Ninja Frog/Run (32x32).png"),
            "jump": load_texture(b"Assets/inside_church/Main Characters/Ninja Frog/Jump (32x32).png"),
            "fall": load_texture(b"Assets/inside_church/Main Characters/Ninja Frog/Fall (32x32).png"),
        }
        self.frame = 0
        self.anim_timer = 0.0
        self.facing_right = True

    def get_current_sprite(self):
        if not self.is_grounded:
            return "jump" if self.vy < 0 else "fall"
        elif self.vx != 0:
            return "run"
        return "idle"

    def draw(self):
        state = self.get_current_sprite()
        tex = self.sprites[state]
        frame_size = 32  # Each frame is 32x32 in the spritesheet
        num_frames = tex.width // frame_size

        self.anim_timer += get_frame_time()
        if self.anim_timer >= 0.1:
            self.anim_timer = 0.0
            self.frame = (self.frame + 1) % num_frames

        # Source rect — flip horizontally if facing left
        fw = frame_size if self.facing_right else -frame_size
        source = Rectangle(self.frame * frame_size, 0, fw, frame_size)
        dest = Rectangle(self.x, self.y, self.width, self.height)
        draw_texture_pro(tex, source, dest, Vector2(0, 0), 0.0, WHITE)
        
    def take_damage(self, amount):
        """Reduce health by amount (clamped to 0)."""
        self.health = max(0, self.health - amount)

    def get_rect(self):
        """Returns the player's collision bounding box (top-left, width, height)."""
        return (self.x, self.y, self.width, self.height)

    def update(self, delta_time, level):
        # 1. Handle Input (Horizontal Movement)
        self.vx = 0.0
        if is_key_down(KEY_LEFT) or is_key_down(KEY_A):
            self.vx = -PLAYER_SPEED
        if is_key_down(KEY_RIGHT) or is_key_down(KEY_D):
            self.vx = PLAYER_SPEED

        # --- Velocity Zeroing for Stability ---
        if self.is_grounded:
            self.vy = 0.0

        # 2. Handle Input (Jump)
        if is_key_pressed(KEY_SPACE) or is_key_pressed(KEY_UP):
            if self.jump_count < self.max_jumps:
                self.jump_count += 1
                self.vy = JUMP_VELOCITY
            else:
                self.jump_count = 0

        # 3. Apply Gravity
        self.vy += GRAVITY * delta_time
        if self.vy > 1000:
            self.vy = 1000

        # --- Reset grounded state at start of frame update ---
        self.is_grounded = False

        # 4. Apply Movement
        self.x += self.vx * delta_time
        self.handle_tile_collision(level, 'X')

        self.y += self.vy * delta_time
        self.handle_tile_collision(level, 'Y')

        # --- Safety Clamp to World Bounds ---
        from level import WORLD_WIDTH
        self.x = max(0, min(self.x, WORLD_WIDTH - self.width))

    def handle_tile_collision(self, level, axis):
        """Performs AABB collision checks against solid tiles and resolves the collision."""
        from level import TILE_ROWS, TILE_COLS
        player_rect = self.get_rect()
        px, py, pw, ph = player_rect

        min_col = int(px / TILE_SIZE)
        max_col = int((px + pw) / TILE_SIZE)
        min_row = int(py / TILE_SIZE)
        max_row = int((py + ph) / TILE_SIZE)

        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):

                if row < 0 or row >= TILE_ROWS or col < 0 or col >= TILE_COLS:
                    continue

                if level[row][col] == TILE_SOLID:
                    tile_rect = (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)

                    if check_collision_recs(player_rect, tile_rect):

                        if axis == 'X':
                            if self.vx > 0:  # Moving Right
                                self.x = tile_rect[0] - self.width
                            elif self.vx < 0:  # Moving Left
                                self.x = tile_rect[0] + TILE_SIZE
                            self.vx = 0.0

                        elif axis == 'Y':
                            if self.vy >= 0:  # Falling (Hitting Ground)
                                self.y = tile_rect[1] - self.height
                                self.is_grounded = True
                            elif self.vy < 0:  # Jumping (Hitting Ceiling)
                                self.y = tile_rect[1] + TILE_SIZE

                            self.vy = 0.0

                        player_rect = self.get_rect()
                        px, py, pw, ph = player_rect

    def check_collection(self, collectibles):
        """Checks for collision with coins and returns indices of collected coins."""
        collected_indices = []
        player_rect = self.get_rect()
        coin_collision_size = TILE_SIZE * 0.5

        for i, (cx, cy) in enumerate(collectibles):
            coin_x = cx - coin_collision_size / 2
            coin_y = cy - coin_collision_size / 2
            coin_rect = (coin_x, coin_y, coin_collision_size, coin_collision_size)

            if check_collision_recs(player_rect, coin_rect):
                collected_indices.append(i)

        return collected_indices

    def check_enemy_collision(self, enemies):
        player_rect = self.get_rect()
        py, ph = player_rect

        for i, enemy in enumerate(enemies):
            enemy_rect = enemy.get_rect()

            if check_collision_recs(player_rect, enemy_rect):
                is_stompable_zone = py + ph < enemy.y + enemy.height * 0.5

                if self.vy > 0 and is_stompable_zone:
                    return "STOMP", i
                else:
                    return "LETHAL", i

        return None, -1

    def reset(self):
        """Resets the player to their starting position."""
        self.x = self.start_x
        self.y = self.start_y
        self.vx = 0.0
        self.vy = 0.0
        self.is_grounded = False
        self.jump_count = 0

