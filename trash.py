import pyray as rl
from pyray import Vector2, Rectangle, Color

# --- Constants ---
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
PLAYER_SPEED = 300.0
JUMP_SPEED = 500.0
GRAVITY = 900.0

# --- Setup ---
rl.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Vertical 2D Platformer")
rl.set_target_fps(60)

# Player
player_pos = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100)
player_vel = Vector2(0, 0)
player_size = Vector2(30, 30)
is_grounded = False

# Platforms (x, y, width, height)
platforms = [
    Rectangle(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20),
    Rectangle(100, 450, 200, 20),
    Rectangle(50, 300, 200, 20),
    Rectangle(150, 150, 200, 20),
    Rectangle(0, 0, 100, 20),
]

# --- Main Game Loop ---
while not rl.window_should_close():
    dt = rl.get_frame_time()

    # --- Update ---
    # Horizontal movement
    if rl.is_key_down(rl.KEY_LEFT) or rl.is_key_down(rl.KEY_A):
        player_pos.x -= PLAYER_SPEED * dt
    if rl.is_key_down(rl.KEY_RIGHT) or rl.is_key_down(rl.KEY_D):
        player_pos.x += PLAYER_SPEED * dt

    # Jump
    if (rl.is_key_pressed(rl.KEY_UP) or rl.is_key_pressed(rl.KEY_SPACE)) and is_grounded:
        player_vel.y = -JUMP_SPEED
        is_grounded = False

    # Apply Gravity
    player_vel.y += GRAVITY * dt
    player_pos.y += player_vel.y * dt

    # Collision detection
    is_grounded = False
    player_rect = Rectangle(player_pos.x, player_pos.y, player_size.x, player_size.y)
    
    for p in platforms:
        if rl.check_collision_recs(player_rect, p):
            if player_vel.y > 0:  # Falling down
                player_pos.y = p.y - player_size.y
                player_vel.y = 0
                is_grounded = True

    # Camera/Scrolling behavior (if player goes too high)
    if player_pos.y < SCREEN_HEIGHT / 2:
        diff = SCREEN_HEIGHT / 2 - player_pos.y
        player_pos.y += diff
        for p in platforms:
            p.y += diff
            # Reset platforms if they go off screen
            if p.y > SCREEN_HEIGHT:
                p.y = -20
                p.x = rl.get_random_value(0, SCREEN_WIDTH - int(p.width))

    # --- Draw ---
    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)

    # Draw Platforms
    for p in platforms:
        rl.draw_rectangle_rec(p, rl.GRAY)

    # Draw Player
    rl.draw_rectangle_v(player_pos, player_size, rl.BLUE)

    rl.draw_text("Vertical Platformer", 10, 10, 20, rl.DARKGRAY)
    rl.end_drawing()

rl.close_window()
