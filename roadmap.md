### Date: 2026/04/08 12:45 PM
**Goal**
implementing double jump in player's update method

**Implementation**
*Technical Plan/Credit*: Use online reference
*Content Credit*: (https://gamemaker.io/en/tutorials/platformer-double-jump)

**Commit message**
Mechanics: double jump on player

Next/To Do:
* Implement winning condition
* Change cross collect to use a coin texture using draw_texture_pro()

### Date: 2026/04/08 2:00 PM
**Goal**
implementing winning condition

**Implementation**
*Technical Plan/Credit*: Use raylib cheatsheet for some functions
*Content Credit*: N/A

**Commit message**
UI/Mechanics: win after you've collected all the collectibles

Next/To Do:
* Organize the code into separate files
* Change cross collect to use a coin texture using draw_texture_pro()


### Date: 2026/04/09 7:00 AM
**Goal**
Restructuring the code into separate classes and files

**Implementation**
*Technical Plan/Credit*: reference midterm project code structure
*Content Credit*: midterm project

**Commit message**
code structure: created constants.py, enemy.py, level.py, player.py, and renderer.py files.

Next/To Do:
* Change cross collect to use a coin texture using draw_texture_pro()


### Date: 2026/04/09 10:00 AM
**Goal**
change cross collect to use a coin texture using draw_texture_pro()

**Implementation**
*Technical Plan/Credit*: Online resource
*Content Credit*: `https://opengameart.org/content/coin-animation`

**Commit message**
Mechanic: replaced crosses with coin texture

Next/To Do:
* Implement screen manager using enum


### Date: 2026/04/15 1:25 PM
**Goal**
Design level one and define its mechanics

**Implementation**
*Technical Plan/Credit*: 
*Content Credit*: 

**Commit message**


Next/To Do:
* improve the GDD_V1 file


### Date: 2026/04/15 11:25 PM
**Goal**
improve the GDD_V1 file

**Implementation**
*Technical Plan/Credit*: 
*Content Credit*: 

**Commit message**
Documentation: "Added level pictures and planned per-level game mechanics"

Next/To Do:
* Write the game base code (skeleton)/recycle the starter code to match my theme


### Date: 2026/04/17 2:00 PM
**Goal**
Draw game background (level 1) to match the theme

**Implementation**
*Technical Plan/Credit*: 
*Content Credit*: 

**Commit message**
UI: "Drew/loaded sprites into the predefined rectangular positions"

Next/To Do:
* Replace coins with theme-based collectibles

### Date: 2026/04/18 8:00 AM
**Goal**
Replace coins with theme-based collectibles

**Implementation**
*Technical Plan/Credit*: 
*Content Credit*: 

**Commit message**
UI: "Added fruit collectibles"

Next/To Do:
* Implement a screen manager like the one from midterm project


### Date: 2026/04/19 9:00 AM
**Goal**
Implement a screen manager like the one from midterm project

**Implementation**
*Technical Plan/Credit*: 
*Content Credit*: 

**Commit message**
UI: "Added fruit collectibles"

Next/To Do:
* Replace coins with theme-specific collectibles

### Date: 2026/04/19 9:00 AM
**Goal**
Replace lives system with a health bar and fix instant game-over bug

**Implementation**
*Technical Plan/Credit*: 
*Content Credit*: 

**Commit message**
UI&Mechanics: 
- Add Player.health (100 HP max) and take_damage(amount); health persists
  across respawns within a run so damage accumulates throughout
- Enemy hit deducts 10 HP instead of consuming a life; game over
  triggers only when health reaches 0 (after 10 hits)
- Draw a colour-coded HP bar in the HUD (green → orange → red) with a
  numeric HP readout; score moved to top-right
- Remove stale jump-count draw_text debug call from Player.update
- Move all enemy spawns to the second half of the level (col 25+) so
  the player has a safe start zone; fixes the immediate game-over caused
  by an enemy sharing the player's spawn tile at row 14 col 2


Next/To Do:
* Replace coins with theme-specific collectibles
* improve enemy logic