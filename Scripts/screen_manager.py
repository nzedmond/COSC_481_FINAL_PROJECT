from pyray import *
from constants import *
from level import parse_level, LEVEL, WORLD_WIDTH, WORLD_HEIGHT
from player import Player
from renderer import draw_level, draw_coins, update_camera, draw_parallax_layer
from enemy import Bullet


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
        self.coin_sheet = load_texture(b"Assets/inside_church/Items/Fruits/Apple.png")
        self.start_tex  = load_texture(b"Assets/inside_church/Items/Checkpoints/Start/Start (Moving) (64x64).png")

    def unload(self):
        for attr in ("bg0", "bg1", "grass_bg1", "grass_bg2", "tiles", "coin_sheet", "start_tex"):
            unload_texture(getattr(self, attr))


# ---------------------------------------------------------------------------
# Helper — draw the four parallax layers given a camera x position
# ---------------------------------------------------------------------------

def _draw_backgrounds(res, cam_x):
    draw_parallax_layer(res.bg0,       cam_x, 0.05, SCREEN_WIDTH, SCREEN_HEIGHT)
    draw_parallax_layer(res.bg1,       cam_x, 0.15, SCREEN_WIDTH, SCREEN_HEIGHT)
    draw_parallax_layer(res.grass_bg1, cam_x, 0.30, SCREEN_WIDTH, SCREEN_HEIGHT)
    draw_parallax_layer(res.grass_bg2, cam_x, 0.50, SCREEN_WIDTH, SCREEN_HEIGHT)


# ---------------------------------------------------------------------------
# Menu screen
# ---------------------------------------------------------------------------

class MenuScreen:
    def __init__(self, manager, res):
        self.manager    = manager
        self.res        = res
        self.bg_x       = 0.0   # slowly pans right to animate the background
        self.blink_t    = 0.0
        self.blink_vis  = True

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

        # Darkening vignette so text is always readable
        draw_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, Color(0, 0, 0, 110))

        # Title
        title = b"Crossing Kabgayi"
        sub   = b"The Broken Sanctuary"
        title_y = SCREEN_HEIGHT // 3 - 20
        draw_text(title, SCREEN_WIDTH // 2 - measure_text(title, 52) // 2,
                  title_y, 52, WHITE)
        draw_text(sub, SCREEN_WIDTH // 2 - measure_text(sub, 26) // 2,
                  title_y + 58, 26, LIGHTGRAY)

        # Blinking prompt
        if self.blink_vis:
            prompt = b"Press ENTER to Start"
            draw_text(prompt, SCREEN_WIDTH // 2 - measure_text(prompt, 26) // 2,
                      SCREEN_HEIGHT * 2 // 3, 26, WHITE)

        # Controls hint at the bottom
        hint = b"Move: Arrows / WASD     Jump: SPACE     Pause: P"
        draw_text(hint, SCREEN_WIDTH // 2 - measure_text(hint, 16) // 2,
                  SCREEN_HEIGHT - 36, 16, GRAY)

        end_drawing()


# ---------------------------------------------------------------------------
# Gameplay screen
# ---------------------------------------------------------------------------

class GameplayScreen:
    def __init__(self, manager, res):
        self.manager = manager
        self.res     = res
        self._init_game()

    def _init_game(self):
        """Reset all gameplay state for a fresh run."""
        self.game_level, self.collectibles, _ = parse_level(LEVEL)
        self.player        = Player(TILE_SIZE * 2, TILE_SIZE * 14)
        self.score         = 0
        self.all_collected = False   # True once every apple is picked up
        self.coin_frame    = 0
        self.anim_timer    = 0.0
        self.start_frame   = 0
        self.start_timer   = 0.0

        # Bullet shooter
        self.bullets       = []
        self.shoot_timer   = 0.0
        self.shoot_interval = 2.0   # seconds between shots

        self.camera          = Camera2D()
        self.camera.target   = Vector2(self.player.x, self.player.y)
        self.camera.offset   = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.camera.rotation = 0.0
        self.camera.zoom     = 1.0

    def on_enter(self, restart=False, **kwargs):
        if restart:
            self._init_game()

    def update(self, dt):
        # Animate coins
        self.anim_timer += dt
        if self.anim_timer >= 0.1:
            self.anim_timer  = 0.0
            self.coin_frame  = (self.coin_frame + 1) % 17  # Apple.png has 17 frames

        # Animate start marker
        self.start_timer += dt
        if self.start_timer >= 0.08:
            self.start_timer = 0.0
            self.start_frame = (self.start_frame + 1) % 17  # Start (Moving) has 17 frames

        if is_key_pressed(KEY_P):
            self.manager.switch_to("PAUSED")
            return

        self.player.update(dt, self.game_level)

        update_camera(self.camera, self.player,
                      WORLD_WIDTH, WORLD_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT)

        # --- Bullet shooter: fire from top-right of the visible screen ---
        self.shoot_timer += dt
        if self.shoot_timer >= self.shoot_interval:
            self.shoot_timer = 0.0
            spawn_x = self.camera.target.x + SCREEN_WIDTH  / 2
            spawn_y = self.camera.target.y - SCREEN_HEIGHT / 2
            target_x = self.player.x + self.player.width  / 2
            target_y = self.player.y + self.player.height / 2
            self.bullets.append(Bullet(spawn_x, spawn_y, target_x, target_y))

        for bullet in self.bullets:
            bullet.update(dt, self.game_level)

        # Remove spent bullets
        self.bullets = [b for b in self.bullets if b.active]

        # Collect apples
        collected = self.player.check_collection(self.collectibles)
        for i in sorted(collected, reverse=True):
            self.collectibles.pop(i)
            self.score += 10

        if not self.collectibles:
            self.all_collected = True

        # Win only when ALL apples are collected AND player reaches the finish
        if self.all_collected and self.player.x + self.player.width >= DEST_COL * TILE_SIZE:
            self.manager.switch_to("WIN", score=self.score)
            return

        # Bullet collision
        player_rect = self.player.get_rect()
        for bullet in self.bullets:
            if check_collision_recs(player_rect, bullet.get_rect()):
                bullet.active = False
                self.player.take_damage(10)
                self.player.reset()
                if self.player.health <= 0:
                    self.manager.switch_to("GAME_OVER", score=self.score)
                    return

    def draw_world(self):
        """Draw the gameplay scene without begin/end_drawing.
        Used both by this screen and by PauseScreen as a background."""
        _draw_backgrounds(self.res, self.camera.target.x)

        begin_mode_2d(self.camera)
        draw_level(self.game_level, self.res.tiles)

        # Start marker at player spawn
        if self.res.start_tex.id > 0:
            src  = Rectangle(self.start_frame * 64, 0, 64, 64)
            dest = Rectangle(TILE_SIZE * 2 - 16, TILE_SIZE * 15 - 64, 64, 64)
            draw_texture_pro(self.res.start_tex, src, dest, Vector2(0, 0), 0.0, WHITE)

        draw_coins(self.collectibles, self.res.coin_sheet, self.coin_frame)
        for bullet in self.bullets:
            bullet.draw()
        self.player.draw()

        # Finish-line marker — glows green once all apples are collected
        fx = DEST_COL * TILE_SIZE
        fy = 10 * TILE_SIZE          # top of the marker (a few tiles above ground)
        fh = 5 * TILE_SIZE           # height of the coloured zone
        pole_color  = GREEN if self.all_collected else Color(160, 160, 160, 200)
        flag_color  = GREEN if self.all_collected else Color(100, 100, 100, 180)
        draw_rectangle(fx + TILE_SIZE // 2 - 3, fy, 6, fh, pole_color)           # pole
        draw_rectangle(fx + TILE_SIZE // 2 + 3, fy, TILE_SIZE, TILE_SIZE, flag_color)  # flag
        label = b"FINISH" if self.all_collected else b"FINISH"
        draw_text(label, fx - measure_text(label, 16) // 2 + TILE_SIZE // 2,
                  fy + fh + 4, 16, pole_color)

        end_mode_2d()

        # HUD — score (top-right)
        score_text = f"Score: {self.score}".encode()
        draw_text(score_text,
                  SCREEN_WIDTH - measure_text(score_text, 20) - 10, 10, 20, WHITE)

        # HUD — health bar (top-left)
        bar_x, bar_y, bar_w, bar_h = 10, 10, 200, 18
        hp_pct = self.player.health / self.player.max_health
        if hp_pct > 0.6:
            bar_color = GREEN
        elif hp_pct > 0.3:
            bar_color = ORANGE
        else:
            bar_color = RED
        draw_rectangle(bar_x, bar_y, bar_w, bar_h, Color(40, 40, 40, 200))          # background
        draw_rectangle(bar_x, bar_y, int(bar_w * hp_pct), bar_h, bar_color)          # fill
        draw_rectangle_lines(bar_x, bar_y, bar_w, bar_h, WHITE)                      # border
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

        # Frozen gameplay behind the overlay
        self.manager.screens["PLAYING"].draw_world()

        # Semi-transparent overlay
        draw_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, Color(0, 0, 0, 160))

        title = b"PAUSED"
        draw_text(title,
                  SCREEN_WIDTH // 2 - measure_text(title, 52) // 2,
                  SCREEN_HEIGHT // 2 - 80, 52, WHITE)

        resume = b"P  -  Resume"
        menu   = b"M  -  Quit to Menu"
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
        # Start from where the camera was when the player died
        self.bg_x  = self.manager.screens["PLAYING"].camera.target.x

    def update(self, dt):
        self.bg_x += 30 * dt   # slow drift

        if is_key_pressed(KEY_R):
            self.manager.switch_to("PLAYING", restart=True)
        elif is_key_pressed(KEY_M):
            self.manager.switch_to("MENU")

    def draw(self):
        begin_drawing()
        clear_background(BLACK)

        _draw_backgrounds(self.res, self.bg_x)
        draw_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, Color(0, 0, 0, 150))

        title = b"GAME OVER"
        draw_text(title,
                  SCREEN_WIDTH // 2 - measure_text(title, 60) // 2,
                  SCREEN_HEIGHT // 3 - 20, 60, RED)

        score_text = f"Score: {self.score}".encode()
        draw_text(score_text,
                  SCREEN_WIDTH // 2 - measure_text(score_text, 28) // 2,
                  SCREEN_HEIGHT // 3 + 58, 28, WHITE)

        restart = b"R  -  Play Again"
        menu    = b"M  -  Main Menu"
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

        title = b"YOU WON!"
        draw_text(title,
                  SCREEN_WIDTH // 2 - measure_text(title, 60) // 2,
                  SCREEN_HEIGHT // 3 - 20, 60, GREEN)

        score_text = f"Final Score: {self.score}".encode()
        draw_text(score_text,
                  SCREEN_WIDTH // 2 - measure_text(score_text, 28) // 2,
                  SCREEN_HEIGHT // 3 + 58, 28, WHITE)

        restart = b"R  -  Play Again"
        menu    = b"M  -  Main Menu"
        draw_text(restart, SCREEN_WIDTH // 2 - measure_text(restart, 24) // 2,
                  SCREEN_HEIGHT * 2 // 3, 24, LIGHTGRAY)
        draw_text(menu, SCREEN_WIDTH // 2 - measure_text(menu, 24) // 2,
                  SCREEN_HEIGHT * 2 // 3 + 38, 24, LIGHTGRAY)

        end_drawing()


# ---------------------------------------------------------------------------
# Screen manager — owns all screens and routes update/draw to the active one
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
