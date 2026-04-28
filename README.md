# Crossing Kabgayi: The Broken Sanctuary
COSC 481 Capstone Project: A 2D side-scrolling platformer built with Python and raylib (pyray).

## How to Run
```bash
cd Scripts
python platformerBase.py
```

> **Dependency:** `pip install raylib`

---

## Controls

| Key | Action |
|-----|--------|
| A / Left Arrow | Move left |
| D / Right Arrow | Move right |
| Space / Up Arrow | Jump (double jump supported) |
| P | Pause / Resume |
| R | Restart *(Game Over / Win screens)* |
| M | Return to Main Menu *(Pause / Game Over / Win screens)* |
| Enter | Start game *(Main Menu)* |

---

## Gameplay

The game has two levels. Health carries over between them — you arrive at Level 2 with whatever HP you had at the end of Level 1.

### Level 1 — The Cemetery (Outdoor)
- Navigate a horizontal platformer across a cemetery landscape
- Collect **apples** scattered across the platforms to build your score
- Reach the **key** hidden on the high platform in the top-right corner to exit the level
- **Bullets** are fired toward the player every 2 seconds — use solid tiles as cover
- Each bullet hit deals **10 HP**

### Level 2 — The Church Interior
- Navigate a vertical dungeon inside the church
- Follow directional pointer signs toward the **door** in the top-right corner
- Reach the door to win the game
- Two enemy shooters fire from different positions, creating crossfire — stay behind platforms
- Each bullet hit deals **10 HP**

### Both Levels
- Health does **not** reset between respawns within a run
- Health reaches 0 → **Game Over**

---

## Screens

| Screen | How to reach it |
|--------|----------------|
| **Main Menu** | On launch; animated parallax background with blinking prompt |
| **Level 1** | Press Enter from the menu |
| **Level 2** | Collect the key at the top-right of Level 1 |
| **Paused** | Press P during play |
| **Game Over** | Health drops to 0 |
| **Win** | Reach the door at the top-right of Level 2 |

---

## Project Structure

| File | Purpose |
|------|---------|
| `platformerBase.py` | Window init, main game loop |
| `screen_manager.py` | All screens (Menu, Gameplay, Pause, Game Over, Win) and the `ScreenManager` router |
| `constants.py` | Physics, screen, tile, and tileset constants |
| `level.py` | Level 1 (16×50) and Level 2 (20×50) tilemap data, coin parser, and active-level switcher |
| `player.py` | Player class — movement, AABB collision, sprite animation, health |
| `enemy.py` | `Bullet` class — aimed projectile, tile collision, out-of-bounds pruning |
| `renderer.py` | `draw_parallax_layer`, `draw_level`, `draw_coins`, `update_camera` |

---

## Features

- [x] Screen manager — Menu, Gameplay, Pause, Game Over, Win
- [x] Two levels with shared health and score carry-over
- [x] Level 1 — Cemetery: 4-layer parallax background, church terrain tiles, key pickup win condition
- [x] Level 2 — Church interior: full-screen background image, door win condition, directional pointer signs
- [x] AABB collision detection (axis-separated X/Y passes)
- [x] Double jump
- [x] Animated player sprite (Ninja Frog — idle, run, jump, fall states)
- [x] Animated Start checkpoint sprite at player spawn
- [x] Apple collectibles with animated spritesheet (17-frame rotation)
- [x] Bullet enemies — aimed projectiles blocked by solid tiles; two shooters with staggered intervals in Level 2
- [x] Health bar HUD (green → orange → red as HP drops)
- [x] Score HUD (top-right) and Level indicator (top-centre)
- [x] Pause overlay renders frozen gameplay behind the menu

---

## Asset Credits

Assets sourced from [Pixel Frog](https://pixelfrog-assets.itch.io/) on itch.io:
- **Main Characters** — Ninja Frog spritesheet
- **Fruits** — Apple spritesheet (used as collectibles)
- **Items / Checkpoints** — Start (Moving) spritesheet
- **Cemetery** — Background layers
- **Inside Church** — Terrain tileset, church interior background
- **Key** (`Assets/key.png`) — Level 1 win item
- **Door** (`Assets/door.png`) — Level 2 win item
