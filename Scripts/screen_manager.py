from pyray import *
from constants import *
import level as _level
from level import parse_level, activate_level
from player import Player
from renderer import draw_level, draw_coins, update_camera, draw_parallax_layer
from enemy import Bullet

# ---------------------------------------------------------------------------
# Level 2 door — top-right corner, sitting on the row-2 platform (cols 41-44)
# ---------------------------------------------------------------------------
_L2_DOOR_COL    = 42
_L2_DOOR_ROW    = 1
_L2_DOOR_X      = _L2_DOOR_COL * TILE_SIZE   # 1680 px
_L2_DOOR_Y      = _L2_DOOR_ROW * TILE_SIZE   #   40 px  (just below solid ceiling)
_L2_DOOR_SIZE   = 64                          # sprite is 64 × 64
_L2_DOOR_FRAMES = 8                           # End (Pressed) spritesheet

# Pointer signs: (world_x, world_y, direction)
# 'right' → ptr_right texture;  'up' → ptr_up texture
_L2_POINTERS = [
    (3  * TILE_SIZE, 17 * TILE_SIZE, 'right'),   # spawn area — go right
    (13 * TILE_SIZE, 15 * TILE_SIZE, 'right'),   # low platform — keep right
    (25 * TILE_SIZE, 10 * TILE_SIZE, 'up'),      # mid section  — go up
    (42 * TILE_SIZE, 4  * TILE_SIZE, 'up'),      # near door    — almost there
]


# ---------------------------------------------------------------------------
# Resources — textures loaded once and shared across all screens
# ---------------------------------------------------------------------------

class Resources:
    def __init__(self):
        self.bg0        = load_texture(b"Assets/cemetery/Background_0.png")
        self.bg1        = load_texture(b"Assets/cemetery/Background_1.png")
        self.grass_bg1  = load_texture(b"Assets/cemetery/Grass_background_1.png")
        self.grass_bg2  = load_texture(b"Assets/cemetery/Grass_background_2.png")
        self.tiles      = load_texture(b"Assets/cemetery/Tiles.png")
        self.church_tiles = load_texture(b"Assets/inside_church/Terrain/Terrain (16x16).png")
        self.coin_sheet   = load_texture(b"Assets/inside_church/Items/Fruits/Apple.png")
        self.start_tex    = load_texture(b"Assets/inside_church/Items/Checkpoints/Start/Start (Moving) (64x64).png")
        self.key_tex      = load_texture(b"Assets/outside_church/4 Animated objects/Key.png")
        # Level 2 — door and directional pointer signs
        self.end_tex      = load_texture(b"Assets/inside_church/Items/Checkpoints/End/End (Pressed) (64x64).png")
        self.ptr_right    = load_texture(b"Assets/outside_church/3 Objects/Pointers/1.png")
        self.ptr_up       = load_texture(b"Assets/outside_church/3 Objects/Pointers/7.png")

    def unload(self):
        for attr in ("bg0", "bg1", "grass_bg1", "grass_bg2", "tiles", "church_tiles",
                     "coin_sheet", "start_tex", "key_tex", "end_tex", "ptr_right", "ptr_up"):
            unload_texture(getattr(self, attr))


# ---------------------------------------------------------------------------
# Background helpers
# ---------------------------------------------------------------------------

def _draw_backgrounds(res, cam_x):
    draw_parallax_layer(res.bg0,       cam_x, 0.05, SCREEN_WIDTH, SCREEN_HEIGHT)
    draw_parallax_layer(res.bg1,       cam_x, 0.15, SCREEN_WIDTH, SCREEN_HEIGHT)
    draw_parallax_layer(res.grass_bg1, cam_x, 0.30, SCREEN_WIDTH, SCREEN_HEIGHT)
    draw_parallax_layer(res.grass_bg2, cam_x, 0.50, SCREEN_WIDTH, SCREEN_HEIGHT)


def _draw_church_background():
    """Solid dark-stone background for the church/dungeon level."""
    draw_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, Color(18, 14, 28, 255))


# ---------------------------------------------------------------------------
# Menu screen
# ---------------------------------------------------------------------------

class MenuScreen:
    def __init__(self, manager, res):
        self.manager = manager
        self.res = res
        self.bg_x = 0.0
        self.blink_t = 0.0
        self.blink_vis = True

    def on_enter(self, **kwargs):
        pass

    def update(self, dt):
        self.bg_x  += 60 * dt
        self.blink_t += dt
        if self.blink_t >= 0.55:
            self.blink_t   = 0.0
            self.blink_vis = not self.blink_vis

        if is_key_pressed(KEY_ENTER):
            self.manager.switch_to("PLAYING", restart=True)

    def draw(self):
        begin_drawing()
        clear_background(BLACK)
        _draw_backgrounds(self.res, self.bg_x)
        draw_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, Color(0, 0, 0, 110))

        title = b"Crossing Kabgayi"
        sub   = b"The Broken Sanctuary"
        title_y = SCREEN_HEIGHT // 3 - 20
        draw_text(title, SCREEN_WIDTH // 2 - measure_text(title, 52) // 2,
                  title_y, 52, WHITE)
        draw_text(sub, SCREEN_WIDTH // 2 - measure_text(sub, 26) // 2,
                  title_y + 58, 26, LIGHTGRAY)

        if self.blink_vis:
            prompt = b"Press ENTER to Start"
            draw_text(prompt, SCREEN_WIDTH // 2 - measure_text(prompt, 26) // 2,
                      SCREEN_HEIGHT * 2 // 3, 26, WHITE)

        hint = b"Move: Arrows / WASD     Jump: SPACE     Pause: P"
        draw_text(hint, SCREEN_WIDTH // 2 - measure_text(hint, 16) // 2,
                  SCREEN_HEIGHT - 36, 16, GRAY)
        end_drawing()


# ---------------------------------------------------------------------------
# Gameplay screen
# ---------------------------------------------------------------------------

class GameplayScreen:
    def __init__(self, manager, res):
        self.manager   = manager
        self.res       = res
        self.level_num = 1
        self._init_game(level_num=1)

    def _init_game(self, level_num=1, carry_health=None):
        """Reset all gameplay state; carry_health preserves HP across level transitions."""
        activate_level(level_num)
        self.level_num = level_num

        self.game_level, self.collectibles, _ = parse_level(_level.LEVEL)

        # Spawn position differs per level
        spawn_row = 14 if level_num == 1 else 18
        self.player = Player(TILE_SIZE * 2, TILE_SIZE * spawn_row)

        if carry_health is not None:
            self.player.health = max(1, carry_health)  # arrive alive

        self.score         = 0
        self.all_collected = False
        self.coin_frame    = 0
        self.anim_timer    = 0.0
        self.start_frame   = 0
        self.start_timer   = 0.0

        self.bullets        = []
        self.shoot_timer    = 0.0
        self.shoot_interval = 2.0 if level_num == 1 else 2.5   # L2 gets slightly longer gap
        # Second shooter — level 2 only (fires from bottom-left, creating crossfire)
        self.shoot_timer2    = 1.5   # offset start so both don't fire at once
        self.shoot_interval2 = 3.5

        # Door animation (level 2 only)
        self.end_frame = 0
        self.end_timer = 0.0

        self.camera = Camera2D()
        self.camera.target   = Vector2(self.player.x, self.player.y)
        self.camera.offset   = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.camera.rotation = 0.0
        self.camera.zoom     = 1.0

    def on_enter(self, restart=False, level_num=None, carry_health=None, **kwargs):
        if restart:
            self._init_game(level_num=1)
        elif level_num is not None:
            self._init_game(level_num=level_num, carry_health=carry_health)

    def update(self, dt):
        self.anim_timer += dt
        if self.anim_timer >= 0.1:
            self.anim_timer = 0.0
            self.coin_frame = (self.coin_frame + 1) % 17

        self.start_timer += dt
        if self.start_timer >= 0.08:
            self.start_timer = 0.0
            self.start_frame = (self.start_frame + 1) % 17

        self.end_timer += dt
        if self.end_timer >= 0.1:
            self.end_timer = 0.0
            self.end_frame = (self.end_frame + 1) % _L2_DOOR_FRAMES

        if is_key_pressed(KEY_P):
            self.manager.switch_to("PAUSED")
            return

        self.player.update(dt, self.game_level)

        update_camera(self.camera, self.player,
                      _level.WORLD_WIDTH, _level.WORLD_HEIGHT,
                      SCREEN_WIDTH, SCREEN_HEIGHT)

        # Shooter 1 — top-right of visible screen
        self.shoot_timer += dt
        if self.shoot_timer >= self.shoot_interval:
            self.shoot_timer = 0.0
            spawn_x = self.camera.target.x + SCREEN_WIDTH  / 2
            spawn_y = self.camera.target.y - SCREEN_HEIGHT / 2
            target_x = self.player.x + self.player.width  / 2
            target_y = self.player.y + self.player.height / 2
            self.bullets.append(Bullet(spawn_x, spawn_y, target_x, target_y))

        # Shooter 2 — bottom-left of visible screen (level 2 only)
        if self.level_num == 2:
            self.shoot_timer2 += dt
            if self.shoot_timer2 >= self.shoot_interval2:
                self.shoot_timer2 = 0.0
                spawn_x = self.camera.target.x - SCREEN_WIDTH  / 2
                spawn_y = self.camera.target.y + SCREEN_HEIGHT / 2
                target_x = self.player.x + self.player.width  / 2
                target_y = self.player.y + self.player.height / 2
                self.bullets.append(Bullet(spawn_x, spawn_y, target_x, target_y))

        for bullet in self.bullets:
            bullet.update(dt, self.game_level)
        self.bullets = [b for b in self.bullets if b.active]

        # Apple collection (contributes to score on both levels)
        collected = self.player.check_collection(self.collectibles)
        for i in sorted(collected, reverse=True):
            self.collectibles.pop(i)
            self.score += 10

        if not self.collectibles:
            self.all_collected = True

        player_rect = self.player.get_rect()

        # Win conditions differ per level
        if self.level_num == 1:
            if self.all_collected and self.player.x + self.player.width >= DEST_COL * TILE_SIZE:
                self.manager.switch_to("PLAYING", level_num=2, carry_health=self.player.health)
                return
        else:
            # Level 2: reach the End door in the top-right corner (no apple requirement)
            door_rect = (_L2_DOOR_X, _L2_DOOR_Y, _L2_DOOR_SIZE, _L2_DOOR_SIZE)
            if check_collision_recs(player_rect, door_rect):
                self.manager.switch_to("WIN", score=self.score)
                return

        for bullet in self.bullets:
            if check_collision_recs(player_rect, bullet.get_rect()):
                bullet.active = False
                self.player.take_damage(10)
                self.player.reset()
                if self.player.health <= 0:
                    self.manager.switch_to("GAME_OVER", score=self.score)
                    return

    def draw_world(self):
        """Draw the gameplay scene (no begin/end_drawing).
        Used by both this screen and PauseScreen as a background."""
        if self.level_num == 2:
            _draw_church_background()
        else:
            _draw_backgrounds(self.res, self.camera.target.x)

        begin_mode_2d(self.camera)

        tile_tex     = self.res.church_tiles if self.level_num == 2 else self.res.tiles
        tile_variant = 'church' if self.level_num == 2 else 'cemetery'
        draw_level(self.game_level, tile_tex, variant=tile_variant)

        # Start marker at player spawn
        if self.res.start_tex.id > 0:
            src  = Rectangle(self.start_frame * 64, 0, 64, 64)
            dest = Rectangle(TILE_SIZE * 2 - 16, TILE_SIZE * (15 if self.level_num == 1 else 19) - 64, 64, 64)
            draw_texture_pro(self.res.start_tex, src, dest, Vector2(0, 0), 0.0, WHITE)

        draw_coins(self.collectibles, self.res.coin_sheet, self.coin_frame)
        for bullet in self.bullets:
            bullet.draw()
        self.player.draw()

        if self.level_num == 1 and self.res.key_tex.id > 0:
            src  = Rectangle(DEST_COL * TILE_SIZE, 10 * TILE_SIZE, 120, 120)
            dest = Rectangle(DEST_COL * 2 - 16, TILE_SIZE * 15, 120, 120)
            draw_texture_pro(self.res.key_tex, src, dest, Vector2(0, 0), 0.0, WHITE)

        if self.level_num == 2:
            # Animated End door in top-right corner
            if self.res.end_tex.id > 0:
                src  = Rectangle(self.end_frame * _L2_DOOR_SIZE, 0, _L2_DOOR_SIZE, _L2_DOOR_SIZE)
                dest = Rectangle(_L2_DOOR_X, _L2_DOOR_Y, _L2_DOOR_SIZE, _L2_DOOR_SIZE)
                draw_texture_pro(self.res.end_tex, src, dest, Vector2(0, 0), 0.0, WHITE)

            # Directional pointer signs guiding toward the door
            for (wx, wy, direction) in _L2_POINTERS:
                tex = self.res.ptr_right if direction == 'right' else self.res.ptr_up
                if tex.id > 0:
                    src  = Rectangle(0, 0, tex.width, tex.height)
                    dest = Rectangle(wx, wy, TILE_SIZE, TILE_SIZE)
                    draw_texture_pro(tex, src, dest, Vector2(0, 0), 0.0, WHITE)

        end_mode_2d()

        # HUD — score (top-right)
        score_text = f"Score: {self.score}".encode()
        draw_text(score_text,
                  SCREEN_WIDTH - measure_text(score_text, 20) - 10, 10, 20, WHITE)

        # HUD — level indicator (top-centre)
        lvl_text = f"Level {self.level_num}".encode()
        draw_text(lvl_text,
                  SCREEN_WIDTH // 2 - measure_text(lvl_text, 20) // 2, 10, 20, LIGHTGRAY)

        # HUD — health bar (top-left)
        bar_x, bar_y, bar_w, bar_h = 10, 10, 200, 18
        hp_pct = self.player.health / self.player.max_health
        bar_color = GREEN if hp_pct > 0.6 else (ORANGE if hp_pct > 0.3 else RED)
        draw_rectangle(bar_x, bar_y, bar_w, bar_h, Color(40, 40, 40, 200))
        draw_rectangle(bar_x, bar_y, int(bar_w * hp_pct), bar_h, bar_color)
        draw_rectangle_lines(bar_x, bar_y, bar_w, bar_h, WHITE)
        hp_label = f"HP  {self.player.health}/{self.player.max_health}".encode()
        draw_text(hp_label, bar_x + 4, bar_y + 1, 16, WHITE)

    def draw(self):
        begin_drawing()
        clear_background(BLACK)
        self.draw_world()
        end_drawing()


# ---------------------------------------------------------------------------
# Pause screen
# ---------------------------------------------------------------------------

class PauseScreen:
    def __init__(self, manager, res):
        self.manager = manager
        self.res     = res

    def on_enter(self, **kwargs):
        pass

    def update(self, dt):
        if is_key_pressed(KEY_P):
            self.manager.switch_to("PLAYING")
        elif is_key_pressed(KEY_M):
            self.manager.switch_to("MENU")

    def draw(self):
        begin_drawing()
        clear_background(BLACK)
        self.manager.screens["PLAYING"].draw_world()
        draw_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, Color(0, 0, 0, 160))

        title  = b"PAUSED"
        resume = b"P  -  Resume"
        menu   = b"M  -  Quit to Menu"
        draw_text(title,
                  SCREEN_WIDTH // 2 - measure_text(title, 52) // 2,
                  SCREEN_HEIGHT // 2 - 80, 52, WHITE)
        draw_text(resume, SCREEN_WIDTH // 2 - measure_text(resume, 26) // 2,
                  SCREEN_HEIGHT // 2 + 10, 26, LIGHTGRAY)
        draw_text(menu, SCREEN_WIDTH // 2 - measure_text(menu, 26) // 2,
                  SCREEN_HEIGHT // 2 + 50, 26, LIGHTGRAY)
        end_drawing()


# ---------------------------------------------------------------------------
# Game Over screen
# ---------------------------------------------------------------------------

class GameOverScreen:
    def __init__(self, manager, res):
        self.manager = manager
        self.res     = res
        self.score   = 0
        self.bg_x    = 0.0

    def on_enter(self, score=0, **kwargs):
        self.score = score
        self.bg_x  = self.manager.screens["PLAYING"].camera.target.x

    def update(self, dt):
        self.bg_x += 30 * dt
        if is_key_pressed(KEY_R):
            self.manager.switch_to("PLAYING", restart=True)
        elif is_key_pressed(KEY_M):
            self.manager.switch_to("MENU")

    def draw(self):
        begin_drawing()
        clear_background(BLACK)
        _draw_backgrounds(self.res, self.bg_x)
        draw_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, Color(0, 0, 0, 150))

        title      = b"GAME OVER"
        score_text = f"Score: {self.score}".encode()
        restart    = b"R  -  Play Again"
        menu       = b"M  -  Main Menu"
        draw_text(title,
                  SCREEN_WIDTH // 2 - measure_text(title, 60) // 2,
                  SCREEN_HEIGHT // 3 - 20, 60, RED)
        draw_text(score_text,
                  SCREEN_WIDTH // 2 - measure_text(score_text, 28) // 2,
                  SCREEN_HEIGHT // 3 + 58, 28, WHITE)
        draw_text(restart, SCREEN_WIDTH // 2 - measure_text(restart, 24) // 2,
                  SCREEN_HEIGHT * 2 // 3, 24, LIGHTGRAY)
        draw_text(menu, SCREEN_WIDTH // 2 - measure_text(menu, 24) // 2,
                  SCREEN_HEIGHT * 2 // 3 + 38, 24, LIGHTGRAY)
        end_drawing()


# ---------------------------------------------------------------------------
# Win screen
# ---------------------------------------------------------------------------

class WinScreen:
    def __init__(self, manager, res):
        self.manager = manager
        self.res     = res
        self.score   = 0
        self.bg_x    = 0.0

    def on_enter(self, score=0, **kwargs):
        self.score = score
        self.bg_x  = self.manager.screens["PLAYING"].camera.target.x

    def update(self, dt):
        self.bg_x += 30 * dt
        if is_key_pressed(KEY_R):
            self.manager.switch_to("PLAYING", restart=True)
        elif is_key_pressed(KEY_M):
            self.manager.switch_to("MENU")

    def draw(self):
        begin_drawing()
        clear_background(BLACK)
        _draw_backgrounds(self.res, self.bg_x)
        draw_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, Color(0, 0, 0, 120))

        title      = b"YOU MADE IT! THE CHURCH IS SAFE."
        score_text = f"Apples Collected: {self.score}".encode()
        restart    = b"R  -  Play Again"
        menu       = b"M  -  Return Home"
        draw_text(title,
                  SCREEN_WIDTH // 2 - measure_text(title, 22) // 2,
                  SCREEN_HEIGHT // 3 - 20, 22, GREEN)
        draw_text(score_text,
                  SCREEN_WIDTH // 2 - measure_text(score_text, 28) // 2,
                  SCREEN_HEIGHT // 3 + 58, 28, WHITE)
        draw_text(restart, SCREEN_WIDTH // 2 - measure_text(restart, 24) // 2,
                  SCREEN_HEIGHT * 2 // 3, 24, LIGHTGRAY)
        draw_text(menu, SCREEN_WIDTH // 2 - measure_text(menu, 24) // 2,
                  SCREEN_HEIGHT * 2 // 3 + 38, 24, LIGHTGRAY)
        end_drawing()


# ---------------------------------------------------------------------------
# Screen manager
# ---------------------------------------------------------------------------

class ScreenManager:
    def __init__(self, res):
        self.screens = {
            "MENU":      MenuScreen(self, res),
            "PLAYING":   GameplayScreen(self, res),
            "PAUSED":    PauseScreen(self, res),
            "GAME_OVER": GameOverScreen(self, res),
            "WIN":       WinScreen(self, res),
        }
        self.current = "MENU"

    def switch_to(self, name, **kwargs):
        self.current = name
        screen = self.screens[name]
        if hasattr(screen, "on_enter"):
            screen.on_enter(**kwargs)

    def update(self, dt):
        self.screens[self.current].update(dt)

    def draw(self):
        self.screens[self.current].draw()
