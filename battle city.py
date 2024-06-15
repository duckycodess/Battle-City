import enum
import pyxel
import pyxelgrid as pg
import os
import random
from tank import Tank
from dataclasses import dataclass
from bullets import Bullets
from enemies import Enemies
from blocks import Block

@dataclass
class CellState:
    type: int

class GameState(enum.Enum):
    READY = 0
    RUNNING = 1
    GAME_OVER = 2
    WIN = 3

class Blocks(enum.Enum):
    EMPTY = 0
    STONE = 1
    BRICK = 2
    MIRROR_NE = 3
    MIRROR_SE = 4
    WATER = 5

class Sound(enum.Enum):
    SHOOT_SOUND = 0
    COLLISION_SOUND = 1
    DEAD_SOUND = 2

class Players(enum.Enum):
    PLAYER = 0
    ENEMY_TANK_1 = 1
    ENEMY_TANK_2 = 2

class BattleCity(pg.PyxelGrid[CellState]):
    def __init__(self):
        super().__init__(r=16, c=16, dim=16)
        self.resource_file = os.path.join(os.path.dirname(__file__), "resources.pyxres")
        self.enemies = Enemies()
        self.bullets = Bullets()
        self.blocks = Block()
        self.state = GameState.READY
        self.score = 0

    def init(self):
        # Loading Resources
        pyxel.load(self.resource_file)
        self.tank = Tank(random.randint(0, self.r - 1) * self.dim, random.randint(0, self.c - 1) * self.dim)  # Tank Spawn

        for r in range(self.r):
            for c in range(self.c):
                if random.randint(0, 50) == 4:
                    self[r, c] = CellState(Blocks.STONE)
                    self.blocks.blocks.append((self.x(r), self.y(c), Blocks.STONE.value))
                elif random.randint(0, 50) == 4:
                    self[r, c] = CellState(Blocks.BRICK)
                    self.blocks.blocks.append((self.x(r), self.y(c), Blocks.BRICK.value))
                elif random.randint(0, 50) == 4:
                    self[r, c] = CellState(Blocks.MIRROR_NE)
                    self.blocks.blocks.append((self.x(r), self.y(c), Blocks.MIRROR_NE.value))
                elif random.randint(0, 50) == 4:
                    self[r, c] = CellState(Blocks.MIRROR_SE)
                    self.blocks.blocks.append((self.x(r), self.y(c), Blocks.MIRROR_SE.value))
                else:
                    self[r, c] = CellState(Blocks.EMPTY)
        self.state = GameState.RUNNING

    def check_block_collission(self, x: int, y: int) -> bool:
        for ax, ay, _ in self.blocks.blocks:
            if (ax < x < ax+self.dim or ax < x +self.dim < ax+self.dim or ax < x +self.dim//2 < ax+self.dim) and \
                (ay < y < ay+self.dim or ay < y+self.dim < ay+self.dim or ay < y+self.dim//2 < ay+self.dim):
                return True
        return False

    def check_bullet_collision(self):
        new_enemy: list[tuple[tuple[int, int], str, str]] = [] # Storage of enemies if hit or not
        for (ax, ay), d, enemy_id in self.enemies.enemy_tank:
            hit = False
            new_bullets: list[tuple[int, int, int, int]] = []
            for bx, by, vx, vy in self.bullets.bullets["player"]:
                if ax < bx < ax + self.dim and ay < by < ay + self.dim: # If bullet hits enemy tank
                    self.score += 10
                    hit = True
                elif self.tank.player_x < bx < self.tank.player_x + self.dim and self.tank.player_y < by < self.tank.player_y + self.dim:
                    self.state = GameState.GAME_OVER
                else:
                    new_bullets.append((bx, by, vx, vy)) # If not hit, keep bullet on screen
            self.bullets.bullets["player"] = new_bullets # Filter out hit bullets
            if not hit: # If enemy not hit, keep on screen
                new_enemy.append(((ax, ay), d, enemy_id))
        self.enemies.enemy_tank = new_enemy # Filter out dead enemies here

        # Enemy bullet checking
        for enemy_id in self.bullets.bullets.keys():
            if enemy_id.startswith("enemy_"):
                new_bullets: list[tuple[int, int, int, int]] = []
                for bx, by, vx, vy in self.bullets.bullets[enemy_id]:
                    if self.tank.player_x < bx < self.tank.player_x + self.dim and self.tank.player_y < by < self.tank.player_y + self.dim:
                        self.state = GameState.GAME_OVER
                    else:
                        new_bullets.append((bx, by, vx, vy))
                self.bullets.bullets[enemy_id] = new_bullets    

    def check_bullet_block_collission(self):
        new_bullets: list[tuple[int, int, int, int]] = []
        for bx, by, vx, vy in self.bullets.bullets["player"]:
            cell_x, cell_y = bx // self.dim, by // self.dim
            if self.in_bounds(cell_x, cell_y):
                cell_type = Blocks(self[cell_x, cell_y].type)
                if cell_type == Blocks.BRICK:
                    new_blocks: list[tuple[int, int, int]] = []
                    for x, y, type in self.blocks.blocks:
                        if type != Blocks.BRICK:
                            new_blocks.append((x, y, type))
                    self[cell_x, cell_y] = CellState(Blocks.EMPTY)
                    self.blocks.blocks = new_blocks
                    continue
                elif cell_type == Blocks.STONE:
                    continue
                elif cell_type == Blocks.MIRROR_NE:
                    vx, vy = vy, vx
                elif cell_type == Blocks.MIRROR_SE:
                    vx, vy = -vy, -vx
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
                            print('hit')
                            new_blocks: list[tuple[int, int, int]] = []
                            for x, y, type in self.blocks.blocks:
                                if type != Blocks.BRICK:
                                    new_blocks.append((x, y, type))
                            self[cell_x, cell_y] = CellState(Blocks.EMPTY)
                            self.blocks.blocks = new_blocks
                            continue
                        elif cell_type == Blocks.STONE:
                            continue
                        elif cell_type == Blocks.MIRROR_NE:
                            vx, vy = vy, vx
                        elif cell_type == Blocks.MIRROR_SE:
                            vx, vy = -vy, -vx
                        new_bullets.append((bx + vx, by + vy, vx, vy))
                self.bullets.bullets[enemy_id] = new_bullets

        self.bullets.check_collision("player", [key for key in self.bullets.bullets.keys() if key.startswith("enemy_")])
    
    def check_enemy_ai(self):
        # Enemy AI basically random movement and firing
        for i, ((ex, ey), d, enemy_id), in enumerate(self.enemies.enemy_tank):
            if random.random() < 0.01:  # 20% chance to change direction
                direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
                d = direction

            if random.random() < 0.1:  # 30% chance to move
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
                if not self.check_block_collission(new_x, new_y):
                    ex, ey = new_x, new_y

            if random.random() < 0.05:  # 20% chance to fire
                self.bullets.fire(enemy_id, ex, ey, d)

            self.enemies.enemy_tank[i] = ((ex, ey), d, enemy_id)

    def update(self):
        if self.state == GameState.GAME_OVER or self.state == GameState.WIN:
            return
        self.tank.update()
        # Tank-Block Collision
        match self.tank.direction:
            case 'UP':
                if not self.check_block_collission(self.tank.player_x, self.tank.move_y):
                    self.tank.player_y = self.tank.move_y
            case 'DOWN':
                if not self.check_block_collission(self.tank.player_x, self.tank.move_y):
                    self.tank.player_y = self.tank.move_y
            case 'LEFT':
                if not self.check_block_collission(self.tank.move_x, self.tank.player_y):
                    self.tank.player_x = self.tank.move_x
            case 'RIGHT':
                if not self.check_block_collission(self.tank.move_x, self.tank.player_y):
                    self.tank.player_x = self.tank.move_x
            case _:
                pass
        # Update tank
        self.bullets.update() # Update bullets
        self.enemies.update() # Update enemies

        # Bullet creation from player
        if pyxel.btnp(pyxel.KEY_SPACE) and not self.bullets.bullets["player"]:
            match self.tank.direction:
                case 'UP':
                    self.bullets.bullets["player"].append((self.tank.player_x + 8, self.tank.player_y, 0, -4))
                case 'DOWN':
                    self.bullets.bullets["player"].append((self.tank.player_x + 8, self.tank.player_y + 14, 0, +4))
                case 'LEFT':
                    self.bullets.bullets["player"].append((self.tank.player_x, self.tank.player_y + 7, -4, 0))
                case 'RIGHT':
                    self.bullets.bullets["player"].append((self.tank.player_x + 14, self.tank.player_y + 7, +4, 0))
                case _:
                    pass
        
        self.check_bullet_block_collission()
        self.check_bullet_collision() # Bullet collision
        self.check_enemy_ai() # Enemy AI
        
        if not self.enemies.enemy_tank:
            self.state = GameState.WIN


    def draw_cell(self, i: int, j: int, x: int, y: int) -> None:
        # Draw the blocks
        pyxel.rect(x, y, 2, 2, pyxel.COLOR_LIME)

        # Block types
        if not self.state == GameState.GAME_OVER:
            self.tank.draw()
        self.enemies.draw()
        self.bullets.draw()

        # Test blocks
        self.blocks.width = self.dim
        self.blocks.draw()

    def pre_draw_grid(self) -> None:
        pyxel.cls(0)
        pyxel.text(5, 5, f"Score: {self.score}", 7)
    
    def post_draw_grid(self) -> None:
        if self.state == GameState.GAME_OVER:
            pyxel.cls(0)
            pyxel.text(128 ,128, 'BOBO', 10)
        elif self.state == GameState.WIN:
            pyxel.cls(4)
            pyxel.text(128 ,128, 'WEIRDASS', 10)

BattleCity().run(title="Battle City", fps=60)