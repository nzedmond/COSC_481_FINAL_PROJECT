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

- Collect **all apples** scattered across the level
- Reach the **finish line** at the far right end of the level
- Both conditions must be met to win — the finish marker glows green once all apples are collected
- **Bullets** are fired from the top-right of the visible screen toward the player every 2 seconds
- Bullets are blocked by solid tiles — use platforms as cover
- Each bullet hit deals **10 HP**; health does not reset between respawns within the same run
- Health reaches 0 → **Game Over**

---

## Screens

| Screen | How to reach it |
|--------|----------------|
| **Main Menu** | On launch; animated parallax background with blinking prompt |
| **Gameplay** | Press Enter from the menu |
| **Paused** | Press P during play |
| **Game Over** | Health drops to 0 |
| **Win** | All apples collected AND finish line reached |

---

## Project Structure

| File | Purpose |
|------|---------|
| `platformerBase.py` | Window init, main game loop |
| `screen_manager.py` | All screens (Menu, Gameplay, Pause, Game Over, Win) and the `ScreenManager` router |
| `constants.py` | Physics, screen, tile, and tileset constants |
| `level.py` | 16×50 tilemap data and coin parser |
| `player.py` | Player class — movement, AABB collision, sprite animation, health |
| `enemy.py` | `Bullet` class — aimed projectile, tile collision, out-of-bounds pruning |
| `renderer.py` | `draw_parallax_layer`, `draw_level`, `draw_coins`, `update_camera` |

---

## Features

- [x] Screen manager — Menu, Gameplay, Pause, Game Over, Win
- [x] Cemetery-themed 4-layer parallax scrolling background
- [x] Tile-based 16×50 level with scrolling Camera2D
- [x] AABB collision detection (axis-separated X/Y passes)
- [x] Double jump
- [x] Animated player sprite (Ninja Frog — idle, run, jump, fall states)
- [x] Animated Start checkpoint sprite at player spawn
- [x] Apple collectibles with animated spritesheet (17-frame rotation)
- [x] Bullet enemy — aimed projectile, blocked by solid tiles
- [x] Health bar HUD (green → orange → red as HP drops)
- [x] Score HUD (top-right)
- [x] Dual win condition — collect all apples AND reach the finish line
- [x] Finish line marker (grey until all apples collected, then glows green)
- [x] Pause overlay renders frozen gameplay behind the menu

---

## Asset Credits

Assets sourced from [Pixel Frog](https://pixelfrog-assets.itch.io/) on itch.io:
- **Main Characters** — Ninja Frog spritesheet
- **Fruits** — Apple spritesheet (used as collectibles)
- **Items / Checkpoints** — Start (Moving) spritesheet
- **Cemetery** — Background layers and tileset
