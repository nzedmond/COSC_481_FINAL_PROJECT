# COSC 481 Final Project
A 2D platformer game built with Python and raylib.

## How to Run
```bash
python platformerBase.py
```

## Controls
| Key | Action |
|-----|--------|
| A / Left Arrow | Move left |
| D / Right Arrow | Move right |
| Space / Up Arrow | Jump (double jump supported) |

## Gameplay
- Collect all coins to win
- Stomp enemies by landing on top of them (+100 pts)
- Touching an enemy from the side or below resets the player (-50 pts)
- Score cannot go below 0

## Project Structure
| File | Purpose |
|------|---------|
| `platformerBase.py` | Game loop and initialization |
| `constants.py` | Physics, screen, and tile constants |
| `level.py` | Level tilemap data and entity parser |
| `player.py` | Player class (movement, collision, input) |
| `enemy.py` | Enemy class (AI, movement, collision) |
| `renderer.py` | Drawing functions and camera logic |

## Features
- [x] Tile-based level with scrolling camera
- [x] AABB collision detection
- [x] Double jump
- [x] Stomp mechanic
- [x] Coin collectibles and scoring
- [x] Win condition (collect all coins)
- [ ] Coin textures (`draw_texture_pro`)
