# Battle City Game

## [HOW TO PLAY]

1. **Objective:** Destroy all enemy tanks and protect your home base.
2. **Controls:**
   - **Move:** Use the arrow keys or the WASD keys to move your tank.
   - **Shoot:** Press the spacebar to shoot bullets.
   - **Restart:** Press R to restart your game without quitting.
3. **Gameplay:** Navigate through different stages, avoiding obstacles and destroying enemy tanks. Protect your home base (the star) from being hit.
4. **Powerups:** While playing the game, you may have powerups to help you accomplish the objective of the game:
   -	`Gatling Mode:` Your tank will automatically shoot bullet continuously for some period of time.
   -	`Invincibility Mode:` Your tank will be invincible from all bullets for some period of time.
   -	`Life:` Getting this powerup will grant you an additional life.

## [STAGE FILE NOTES]
The stage file is a `.py file` that provides the necessary details to create and customize stages, including player spawn points, enemy spawn points, and the layout of each level.
1. **Player and Enemy Spawn Points:** The `player_spawn` and `enemy_spawn` are provided dictionaries that specifies the starting position of the player and the enemies. Players can only be spawned at one location while enemies can have multiple spawn points. The key is the level number, and the value is a tuple representing the row and column coordinates on a 16x16 grid.
2. **Level Layouts:** The `levels` dictionary defines the layout for each level. Each level is specified by its key and its layout by its value. All cells within a 16x16 range should contain a number from 0-8
    Values are as follows:
   - `0`: Empty Cell
   - `1`: Stone Cell
   - `2`: Brick Cell
   - `3`: Mirror (North-East-Leaning)
   - `4`: Mirror (South-East-Leaning)
   - `5`: Water Cell
   - `6`: Cracked Brick Cell
   - `7`: Forest Cell
   - `8`: Home Cell

## [CHEAT CODE]
Activate the cheat code by typing: 
   - `hesoyam`: This will grant you an additional life.
   - `pewpews`: This will activate Gatling Mode.
   - `juancho`: This will clear all enemy tanks in the level.

## HIGHEST PHASE ACCOMPLISHED

**Phase 3**

## MEMBERS and CONTRIBUTIONS

**:P**  
- Implementation of Player and Enemy Tanks Mechanics
- Implementaion of Player Bullets Mechanics
- Implementation of Enemy AI
- Implementation of Collission Mechanics
- Implementation of Game States and Levels
- Cheat Code Implementation
- Stage File Implementation
- Testing and Debugging

**:P**  
- Implementation of Enemy Bullets Mechanics
- Implementation of Collission Mechanics
- Implementation of the Types of Cells
- Stage Design, Gameplay Graphics and Sound Effects
- Implementation of Powerups 
- Implementation of Types of Enemy Tanks
- Testing and Debugging

## VIDEO DEMO

[Google Drive Video Demo]

