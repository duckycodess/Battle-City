import pyxel
import pyxelgrid as pg
import os
import random
from assets.stage import Stage
from blocks import Block
from bullets import Bullets
from dataclasses import dataclass
from enemies import Enemies
from enum import Enum
from tank import Tank
from powerups import Powerup

# Constant Declarations
class GameState(Enum):
    READY = 0
    RUNNING = 1
    GAME_OVER = 2
    WIN = 3
    LOADING_SCREEN = 4
    NEXT_LEVEL = 5
    LEVEL_COMPLETED = 6
    RESPAWN = 7

class Blocks(Enum):
    EMPTY = 0
    STONE = 1
    BRICK = 2
    MIRROR_NE = 3
    MIRROR_SE = 4
    WATER = 5
    CRACKED_BRICK = 6
    FOREST = 7
    HOME = 8
    BORDER = 9

FIRE_BULLET = 0
PLAYER_DIED = 1
ENEMY_KILLED = 2
GAME_WON = 3
GAME_LOST = 4
BULLET_EXPLODE=5
BTN_PRESS = 6
GET_POWERUP = 7


class Powerups(Enum):
    GATLING = 1
    INVISIBILITY = 2
    LIFE = 3

@dataclass
class CellState:
    type: int

class Sound(Enum):
    SHOOT_SOUND = 0
    COLLISION_SOUND = 1
    DEAD_SOUND = 2

class PlayerTypes(Enum):
    PLAYER = 0
    ENEMY_TANK_1 = 1
    ENEMY_TANK_2 = 2


# Main File
class BattleCity(pg.PyxelGrid[CellState]):
    def __init__(self):
        super().__init__(r=18, c=18, dim=16)
        self.resource_file = os.path.join(os.path.dirname(__file__), "assets/resources.pyxres")
        self.score = 0
        self.lives = 3
        self.level = 1
        self.tank_loc_col = 0
        self.tank_loc_row = 0
        self.enemy_spawn_col = 15
        self.enemy_spawn_row = 15
        self.init_positions()
        self.cheat_code = ""
        self.cheat_code_sequence = "hesoyam"
    
        self.key_map = self.generate_key_map()
        self.tick = 0
    
    def init_positions(self, restart: bool=False):
        if restart:
            self.level = 1
        self.bullets = Bullets()
        self.blocks = Block()
        self.powerups = Powerup()
        self.load_stage_file()
        self.enemies_count = 0
        self.enemy_spawning = 0
        self.state = GameState.READY
        self.create_border()
        self.load_level()


    def init(self):
        # Loading Resources
        pyxel.load(self.resource_file)
        self.state = GameState.LOADING_SCREEN


    def load_level(self):
        self.current_level = self.level_layouts[self.level]
        self.populate_blocks()
        self.tank = Tank(self.x(self.tank_loc_col), self.y(self.tank_loc_row))
        self.enemies = Enemies()
        self.enemies_count = 1 #(self.level*2) + 3
        self.enemy_spawning = self.enemies_count
    
    def check_cheat_code(self):
        for key, char in self.key_map.items():
            if pyxel.btnp(key):
                self.cheat_code += char
                if len(self.cheat_code) > len(self.cheat_code_sequence):
                    self.cheat_code = self.cheat_code[-len(self.cheat_code_sequence):]

                if self.cheat_code == 'hesoyam':
                    self.lives += 1
                    self.cheat_code = ""
                elif self.cheat_code == 'pewpews':
                    self.tank.activate_gatling(300)
                    self.cheat_code = ""
                elif self.cheat_code == 'juancho':
                    self.enemies.enemy_tank.clear()
                    self.cheat_code = ""

    def generate_key_map(self) -> dict[int, str]:
        key_map: dict[int, str] = {}
        for i in range(pyxel.KEY_A, pyxel.KEY_Z + 1):
            key_map[i] = chr(i).lower()
        for i in range(pyxel.KEY_0, pyxel.KEY_9 + 1):
            key_map[i] = chr(i)
        return key_map
    
    def create_border(self):
        for r in range(self.r):
            for c in range(self.c):
                if r == 0 or r == self.r - 1 or c == 0 or c == self.c - 1:
                    self[c, r] = CellState(Blocks.BORDER.value)
                    self.blocks.blocks.append((self.x(c), self.y(r), Blocks.BORDER.value))

    def populate_blocks(self):
        for r in range(self.r-2):
            for c in range(self.c-2):
                block_type = int(self.current_level[r][c])
                if self.is_invalid_block_placement(r, c):
                    raise ValueError(f'Invalid block placed or this is a spawn area!, {r}, {c}')
                self[c+1, r+1] = CellState(block_type)
                self.blocks.blocks.append((self.x(c+1), self.y(r+1), block_type))

                if block_type == 0:
                    self.blocks.empty_blocks.append((c+1, r+1))

    def is_invalid_block_placement(self, r: int, c: int) -> bool:
        return (self.current_level[r][c] != '0') and (
                (r+1 == self.tank_loc_row and c+1 == self.tank_loc_col) or
                (r+1 == self.enemy_spawn_row and c+1 == self.enemy_spawn_col))
        

    def load_stage_file(self):
        stage = Stage() # Dito ko kukunin info
        self.level_layouts = stage.levels 
        if self.in_bounds(stage.player_spawn_row, stage.player_spawn_col):
            self.tank_loc_col, self.tank_loc_row = stage.player_spawn_col+1, stage.player_spawn_row+1
        else:
            raise ValueError('invalid row or column!')
        if self.in_bounds(stage.enemy_spawn_row, stage.player_spawn_col):
            self.enemy_spawn_col, self.enemy_spawn_row = stage.enemy_spawn_col+1, stage.enemy_spawn_row+1
        else:
            raise ValueError('invalid row or column!')
            

    def check_block_collission(self, x: int, y: int) -> bool:
        for ax, ay, type in self.blocks.blocks:
            if type and (ax < x < ax+self.dim or ax < x +self.dim < ax+self.dim or ax < x +self.dim//2 < ax+self.dim) and \
                (ay < y < ay+self.dim or ay < y+self.dim < ay+self.dim or ay < y+self.dim//2 < ay+self.dim):
                return True
        return False

    def check_powerup_collission(self, x: int, y: int):
        new_powerups: list[tuple[int,int,int]] = []
        for px, py, t in self.powerups.powerups:
            hit = False
            if (px < x < px+self.dim or px < x +self.dim < px+self.dim or px < x + self.dim//2 < px+self.dim) and \
                (py < y < py+self.dim or py < y +self.dim < py+self.dim or py < y+self.dim//2 < py+self.dim):
                pyxel.play(0, GET_POWERUP)
                hit = True
                if t == 1:
                    self.tank.activate_gatling(300)
                elif t == 2:
                    self.tank.activate_invincibility(300)
                elif t == 3:
                    self.lives += 1
            if not hit:
                new_powerups.append((px, py, t))
        
        self.powerups.powerups = new_powerups

    def check_bullet_collision(self):
        new_enemy: list[tuple[tuple[int, int], str, str, int]] = [] # Storage of enemies if hit or not
        for (ax, ay), d, enemy_id, t in self.enemies.enemy_tank:
            hit = False
            new_bullets: list[tuple[int, int, int, int]] = []
            for bx, by, vx, vy in self.bullets.bullets["player"]:
                if ax < bx < ax + self.dim and ay < by < ay + self.dim: # If bullet hits enemy tank
                    if t == 1:
                        hit = True
                        new_enemy.append(((ax, ay), d, enemy_id, 2))
                        self.score += 50
                    else:
                        if t == 0:
                            self.score += 100
                        elif t == 2:
                            self.score += 200
                        hit = True
                elif self.tank.player_x < bx < self.tank.player_x + self.dim and self.tank.player_y < by < self.tank.player_y + self.dim:
                    pyxel.play(0, PLAYER_DIED)
                    self.lives -= 1
                    if not self.lives:
                        self.state = GameState.GAME_OVER
                        pyxel.play(0, GAME_LOST)
                    else:
                        self.state = GameState.RESPAWN
                else:
                    new_bullets.append((bx, by, vx, vy)) # If not hit, keep bullet on screen
            self.bullets.bullets["player"] = new_bullets # Filter out hit bullets
            if hit:
                pyxel.play(0, ENEMY_KILLED)
            if not hit: # If enemy not hit, keep on screen
                new_enemy.append(((ax, ay), d, enemy_id, t))
        self.enemies.enemy_tank = new_enemy # Filter out dead enemies here

        for enemy_id in self.bullets.bullets.keys():
            if enemy_id.startswith("enemy_"):
                new_bullets: list[tuple[int, int, int, int]] = []
                for bx, by, vx, vy in self.bullets.bullets[enemy_id]:
                    if self.tank.player_x < bx < self.tank.player_x + self.dim and self.tank.player_y < by < self.tank.player_y + self.dim:
                        pyxel.play(0, PLAYER_DIED)
                        self.lives -= 1
                        if not self.lives:
                            self.state = GameState.GAME_OVER
                            pyxel.play(0, GAME_LOST)
                        else:
                            self.state = GameState.RESPAWN
                    else:
                        hit_self = False
                        # if enemy bullet hits itself
                        for (ex, ey), _, eid, _ in self.enemies.enemy_tank:
                            if eid == enemy_id:
                                if ex < bx < ex + self.dim and ey < by < ey + self.dim:
                                    hit_self = True
                                    break
                        if not hit_self:
                            new_bullets.append((bx, by, vx, vy))
                self.bullets.bullets[enemy_id] = new_bullets     

    def check_bullet_block_collission(self):
        new_bullets: list[tuple[int, int, int, int]] = []
        for bx, by, vx, vy in self.bullets.bullets["player"]:
            cell_x, cell_y = pyxel.floor(bx / self.dim), pyxel.floor(by / self.dim)
            if self.in_bounds(cell_x, cell_y):
                cell_type = Blocks(self[cell_x, cell_y].type)

                if cell_type == Blocks.BRICK:
                    pyxel.play(0, BULLET_EXPLODE)
                    for i in reversed(range(len(self.blocks.blocks))):
                        block = self.blocks.blocks[i]
                        if block[2] == Blocks.BRICK.value and block[0] <= bx <= block[0] + self.dim \
                                and block[1] <= by <= block[1] + self.dim:
                            self.blocks.blocks[i] = (self.x(cell_x), self.y(cell_y), Blocks.CRACKED_BRICK.value)
                            self[cell_x, cell_y] = CellState(Blocks.CRACKED_BRICK.value)
                            break
                    continue
                elif cell_type == Blocks.CRACKED_BRICK:
                    pyxel.play(0, BULLET_EXPLODE)
                    for i in reversed(range(len(self.blocks.blocks))):
                        block = self.blocks.blocks[i]
                        if block[2] == Blocks.CRACKED_BRICK.value and block[0] <= bx <= block[0] + self.dim \
                                and block[1] <= by <= block[1] + self.dim:
                            self.blocks.blocks[i] = (self.x(cell_x), self.y(cell_y), Blocks.EMPTY.value)
                            self[cell_x, cell_y] = CellState(Blocks.EMPTY.value)
                            break
                    continue
                elif cell_type == Blocks.STONE: 
                    pyxel.play(0, BULLET_EXPLODE)
                    continue
                elif cell_type == Blocks.BORDER:
                    pyxel.play(0, BULLET_EXPLODE)
                    continue
                elif cell_type == Blocks.MIRROR_NE:
                    vx, vy = vy, vx
                elif cell_type == Blocks.MIRROR_SE:
                    vx, vy = -vy, -vx
                elif cell_type == Blocks.WATER:
                    pass
                new_bullets.append((bx + vx, by + vy, vx, vy))
        self.bullets.bullets["player"] = new_bullets

        # Enemy bullet checking
        for enemy_id in self.bullets.bullets.keys():
            if enemy_id.startswith("enemy_"):
                new_bullets: list[tuple[int, int, int, int]] = []

                for bx, by, vx, vy in self.bullets.bullets[enemy_id]:
                    cell_x, cell_y = bx // self.dim, by // self.dim
                    if self.in_bounds(cell_x, cell_y):
                        cell_type = Blocks(self[cell_x, cell_y].type)

                        if cell_type == Blocks.BRICK:
                            for i in reversed(range(len(self.blocks.blocks))):
                                block = self.blocks.blocks[i]
                                if block[2] == Blocks.BRICK.value and block[0] <= bx <= block[0] + self.dim \
                                        and block[1] <= by <= block[1] + self.dim:
                                    self.blocks.blocks[i] = (self.x(cell_x), self.y(cell_y), Blocks.CRACKED_BRICK.value)
                                    self[cell_x, cell_y] = CellState(Blocks.CRACKED_BRICK.value)
                                    break
                            continue
                        elif cell_type == Blocks.CRACKED_BRICK:
                            for i in reversed(range(len(self.blocks.blocks))):
                                block = self.blocks.blocks[i]
                                if block[2] == Blocks.CRACKED_BRICK.value and block[0] <= bx <= block[0] + self.dim \
                                        and block[1] <= by <= block[1] + self.dim:
                                    self.blocks.blocks[i] = (self.x(cell_x), self.y(cell_y), Blocks.EMPTY.value)
                                    self[cell_x, cell_y] = CellState(Blocks.EMPTY.value)
                                    break
                            continue
                        elif cell_type == Blocks.STONE or cell_type == Blocks.BORDER:
                            continue
                        elif cell_type == Blocks.MIRROR_NE:
                            vx, vy = vy, vx
                        elif cell_type == Blocks.MIRROR_SE:
                            vx, vy = -vy, -vx
                        elif cell_type == Blocks.WATER:
                            pass
                        new_bullets.append((bx + vx, by + vy, vx, vy))
                self.bullets.bullets[enemy_id] = new_bullets

        self.bullets.check_collision("player", [key for key in self.bullets.bullets.keys() if key.startswith("enemy_")])
    
    def is_tank_collision(self, x: int, y: int, width: int, height: int, ignore_tank_id: str = "") -> bool:
        # Check player tank
        if ignore_tank_id != "player" and self.rect_intersect(x, y, width, height, self.tank.player_x, self.tank.player_y, self.tank.width, self.tank.height):
            return True
        # Check enemy tanks
        for (ex, ey), _, enemy_id, _ in self.enemies.enemy_tank:
            if ignore_tank_id != enemy_id and self.rect_intersect(x, y, width, height, ex, ey, self.tank.width, self.tank.height):
                return True
        return False

    def rect_intersect(self, x1: int, y1: int, w1: int, h1: int, x2: int, y2: int, w2: int, h2: int) -> bool:
        return not (x1 > x2 + w2 or x1 + w1 < x2 or y1 > y2 + h2 or y1 + h1 < y2)
    
    def check_enemy_ai(self):
        # Enemy AI basically random movement and firing
        if self.tick % 30:
            for i, ((ex, ey), d, enemy_id, enemy_type), in enumerate(self.enemies.enemy_tank):
                if random.random() < 0.03:  # 20% chance to change direction
                    direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
                    d = direction

                if random.random() < 0.4:  # 30% chance to move
                    new_x, new_y = ex, ey
                    if d == 'UP':
                        new_y = max(ey - 2, 0)
                    elif d == 'DOWN':
                        new_y = min(ey + 2, pyxel.height - self.dim)
                    elif d == 'LEFT':
                        new_x = max(ex - 2, 0)
                    elif d == 'RIGHT':
                        new_x = min(ex + 2, pyxel.width - self.dim)

                    # Check for block collisions
                    if not self.check_block_collission(new_x, new_y) and not self.is_tank_collision(new_x, new_y, self.dim, self.dim, enemy_id):
                        ex, ey = new_x, new_y

                if random.random() < 0.2:  # 20% chance to fire
                    if enemy_id not in self.bullets.bullets or not self.bullets.bullets[enemy_id]:
                        self.bullets.fire(enemy_id, ex, ey, d)

                self.enemies.enemy_tank[i] = ((ex, ey), d, enemy_id, enemy_type)
        if self.tick % 600 == 0 and self.enemy_spawning > 0: # Every 10 seconds spawn an enemy
            self.enemies.enemy_tank.append(((self.x(self.enemy_spawn_col), self.y(self.enemy_spawn_row)), 
            random.choice(['UP',  'DOWN', 'LEFT', 'RIGHT']), f'enemy_{self.enemy_spawning}', random.choice([0,1]))) # Just append the enemy into a list
            self.enemy_spawning -= 1 # Bawasan need to spawn

    def update(self):


        if self.state == GameState.LOADING_SCREEN:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.state = GameState.NEXT_LEVEL
                pyxel.play(0, BTN_PRESS)
        if self.state == GameState.NEXT_LEVEL:
            self.tick += 1
            if not self.tick % 180:
                self.tick = 0
                self.state = GameState.RUNNING
        if self.state == GameState.RESPAWN:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.tank = Tank(self.x(self.tank_loc_col), self.y(self.tank_loc_row))
                self.state = GameState.RUNNING
        
        if self.state == GameState.LEVEL_COMPLETED:
            self.tick += 1
            if self.level <= max(list(self.level_layouts.keys())) and not self.tick % 180:
                self.init_positions()
                self.state = GameState.NEXT_LEVEL
        elif not self.state == GameState.RUNNING:
            return
        
        if self.state == GameState.RUNNING and pyxel.btnp(pyxel.KEY_R):
            pyxel.play(0, BTN_PRESS)
            self.init_positions(restart=True)
            self.tick = 0
            self.state = GameState.LOADING_SCREEN
        
        self.tank.update()
        # Tank-Block Collision
        match self.tank.direction:
            case 'UP':
                if not self.check_block_collission(self.tank.player_x, self.tank.move_y) \
                    and not self.is_tank_collision(self.tank.player_x, self.tank.move_y, self.dim, self.dim, 'player'):
                    self.tank.player_y = self.tank.move_y
            case 'DOWN':
                if not self.check_block_collission(self.tank.player_x, self.tank.move_y) \
                    and not self.is_tank_collision(self.tank.player_x, self.tank.move_y, self.dim, self.dim, 'player'):
                    self.tank.player_y = self.tank.move_y
            case 'LEFT':
                if not self.check_block_collission(self.tank.move_x, self.tank.player_y) \
                    and not self.is_tank_collision(self.tank.move_x, self.tank.player_y, self.dim, self.dim, 'player'):
                    self.tank.player_x = self.tank.move_x
            case 'RIGHT':
                if not self.check_block_collission(self.tank.move_x, self.tank.player_y) \
                    and not self.is_tank_collision(self.tank.move_x, self.tank.player_y, self.dim, self.dim, 'player'):
                    self.tank.player_x = self.tank.move_x
            case _:
                pass
        
        # powerup spawn
        if self.tick % 1000 == 0 :
            self.powerups.timer = self.tick
            spawn_x, spawn_y = random.choice(self.blocks.empty_blocks)
            self.powerups.powerups.append((self.x(spawn_x), self.y(spawn_y), random.choice([0,1,2,3])))
            print(self.powerups.powerups)

        # powerup despawn
        if self.tick - self.powerups.timer == 480 and self.powerups.powerups:
            self.powerups.powerups.pop(0)


        # Handle rapid firing for GATLING mode
        if self.tank.gatling_mode and self.tick % 5 == 0:
            self.bullets.fire('player', self.tank.player_x, self.tank.player_y, self.tank.direction)

        # Regular bullet firing
        if not self.tank.gatling_mode and self.tick != 0 and pyxel.btnp(pyxel.KEY_SPACE) and not self.bullets.bullets["player"]:
            self.bullets.fire('player', self.tank.player_x, self.tank.player_y, self.tank.direction)
            pyxel.play(0, FIRE_BULLET)
        
        # Update tank
         # Update bullets
        self.enemies.update() # Update enemies

        # Bullet creation from player
        if self.tick != 0 and pyxel.btnp(pyxel.KEY_SPACE) and not self.bullets.bullets["player"]:
            self.bullets.fire('player', self.tank.player_x, self.tank.player_y, self.tank.direction)
            pyxel.play(0, FIRE_BULLET)
        self.check_cheat_code()
        
        self.bullets.update()
        self.check_bullet_block_collission()
        self.check_bullet_collision() # Bullet collision
        self.check_enemy_ai() # Enemy AI
        self.check_powerup_collission(self.tank.player_x, self.tank.player_y)

        
        if not self.enemies.enemy_tank and not ([values for values in self.bullets.bullets.values() if values]) \
            and not self.enemy_spawning:
                if self.level < max(list(self.level_layouts.keys())):
                    self.tick = 0
                    self.level += 1
                    self.state = GameState.LEVEL_COMPLETED
                else:
                    self.state = GameState.WIN
                    pyxel.play(0, GAME_WON)

        self.tick += 1

    def draw_cell(self, i: int, j: int, x: int, y: int) -> None:
        pyxel.rect(x, y, 16, 16, 0)

        if self.state == GameState.LOADING_SCREEN:
            pyxel.cls(0)
            pyxel.text(102, 128, 'Press Space to Start', 4)
        elif self.state == GameState.NEXT_LEVEL:
            pyxel.cls(0)
            pyxel.text(120, 110, f"Score: {self.score}", 7)
            pyxel.text(120, 130, f'Lives: {self.lives}', 7)
            if self.tick % 7:
                pyxel.text(110, 150, f'Loading Level {self.level}...', 7)
            elif self.tick % 5:
                pyxel.text(110, 150, f'Loading Level {self.level}..', 7)
            elif self.tick % 3:
                pyxel.text(110, 150, f'Loading Level {self.level}.', 7)
        else:
            self.blocks.width = self.dim

            # Block types
            self.bullets.draw()
            if not self.state == GameState.GAME_OVER:
                self.tank.draw()
            self.enemies.draw()
            self.blocks.draw()
            self.powerups.draw()

    def pre_draw_grid(self) -> None:

        if self.state == GameState.NEXT_LEVEL:
            pyxel.cls(0)
            pyxel.text(100, 110, f"Score: {self.score}", 7)
            pyxel.text(100, 130, f'Lives: {self.lives}', 7)
            pyxel.text(100, 150, f'Loading Level {self.level}', 7)
        elif not self.state == GameState.LOADING_SCREEN:
            pyxel.cls(1)
            pyxel.text(5, 5, f"Score: {self.score}", 7)
            pyxel.text(50, 5, f'Lives: {self.lives}', 7)
            pyxel.text(250, 5, f'Level {self.level}', 7)
    
    def post_draw_grid(self) -> None:
        if self.state == GameState.RESPAWN:
            pyxel.dither(0.9)
            pyxel.rect(0,0, self.x(self.r), self.y(self.c), 1)
            pyxel.dither(1)
            pyxel.text(self.x(8)-30, self.y(8), "Press Space to Respawn", 7)
            
        if self.state not in [GameState.LOADING_SCREEN, GameState.NEXT_LEVEL]:
            pyxel.text(5, 5, f"Score: {self.score}", 7)
            pyxel.text(50, 5, f'Lives: {self.lives}', 7)
            pyxel.text(250, 5, f'Level {self.level}', 7)
        if self.state == GameState.GAME_OVER:
            pyxel.cls(0)
            pyxel.text(self.x(8)-5 ,self.y(8), 'Loser', 10)
        elif self.state == GameState.WIN:
            pyxel.cls(4)
            pyxel.text(self.x(8)-5 ,self.y(8), 'Winner', 8)
            pyxel.text(self.x(8)-30, self.y(8)+10, f'Your Score is: {self.score}', 8)
        
BattleCity().run(title="Battle City", fps=60)