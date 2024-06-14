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

class Sound(enum.Enum):
    SHOOT_SOUND = 0
    COLLISION_SOUND = 1
    DEAD_SOUND = 2

class BattleCity(pg.PyxelGrid[CellState]):
    def __init__(self):
        super().__init__(r=16, c=16, dim=16)
        self.resource_file = os.path.join(os.path.dirname(__file__), "resources.pyxres")
        self.enemies = Enemies()
        self.projectiles = Bullets()
        self.blocks = Block()
        self.state = GameState.READY
        self.score = 0

    def init(self):
        # Loading Resources
        pyxel.load(self.resource_file)
        self.tank = Tank(random.randint(0, self.r - 1), random.randint(0, self.c - 1)) # Tank Spawn

        for r in range(self.r):
            for c in range(self.c):
                self[r, c] = CellState(Blocks.EMPTY) # Creation of Cells
        self.state = GameState.RUNNING

    def check_block_collission(self, x, y, width):
        # False muna ewan q pa
        return False

    def check_bullet_collision(self):
        # Bullet Collission 
        new_enemy: list[tuple[int, int]] = [] # Storage ng enemies if natamaan ba or hindi
        for ax, ay in self.enemies.enemy_tank:
            hit = False
            new_bullets: list[tuple[int, int, int, int]] = []
            for bx, by, vx, vy in self.projectiles.bullets:
                if ax < bx < ax + self.dim and ay < by < ay + self.dim: # Basically for every position ng tank, if nandon yun position ng bullet deads
                    self.score += 10
                    hit = True # Pag in the range this becomes true to be used later
                else:
                    new_bullets.append((bx, by, vx, vy)) # Pag di natamaan, balik natin bullet para nakikita pa rin sa screen
            self.projectiles.bullets = new_bullets # If may mga bullets na nawala nafilter out na kasi di na inappend
            if not hit: # Eto yung to be used later na kanina so if hindi nahit balik lang natin enemy para di mawala sa screen
                new_enemy.append((ax, ay))
        self.enemies.enemy_tank = new_enemy # Filtered out na dead enemies here
    

    def check_enemy_ai(self):
        # Enemy AI basically random movement and firing
        for i, (ex, ey) in enumerate(self.enemies.enemy_tank):
            if random.random() < 0.20:  # 20% chance to change direction
                direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
            else:
                direction = None

            if random.random() < 0.30:  # 30% chance to move
                new_x, new_y = ex, ey
                if direction == 'UP':
                    new_y = max(ey - 2, 0)
                elif direction == 'DOWN':
                    new_y = min(ey + 2, pyxel.height - self.dim)
                elif direction == 'LEFT':
                    new_x = max(ex - 2, 0)
                elif direction == 'RIGHT':
                    new_x = min(ex + 2, pyxel.width - self.dim)

                # Check for block collisions (to be implemented)
                    #if not self.check_block_collission(new_x, new_y, self.width):
                ex, ey = new_x, new_y

            if random.random() < 0.10:  # 20% chance to fire
                self.projectiles.fire(ex, ey, direction)

            self.enemies.enemy_tank[i] = (ex, ey)

    def update(self):
        self.tank.update() # Update whenever sa tank
        self.projectiles.update() # Update sa bullets (both enemy and ours sana)
        self.enemies.update() # Update sa enemies most likely movement and drawing nila sa screen

        # Basically just creation ng bullets and saan magspspawn from the player
        if pyxel.btnp(pyxel.KEY_SPACE):
            match self.tank.direction:
                case 'UP':
                    self.projectiles.bullets.append((self.tank.player_x + 7, self.tank.player_y, 0, -4))
                case 'DOWN':
                    self.projectiles.bullets.append((self.tank.player_x + 7, self.tank.player_y + 8, 0, +4))
                case 'LEFT':
                    self.projectiles.bullets.append((self.tank.player_x, self.tank.player_y + 6, -4, 0))
                case 'RIGHT':
                    self.projectiles.bullets.append((self.tank.player_x + 8, self.tank.player_y + 6, +4, 0))
                case _:
                    pass

        self.check_bullet_collision() # Eto yung bullet collission sa taas
        self.check_enemy_ai() # Enemy AI

    def draw_cell(self, i: int, j: int, x: int, y: int) -> None:
        cell_state = self[i, j]
        # Lagay sana ito sa blocks na file
        pyxel.rect(x, y, 2, 2, pyxel.COLOR_LIME)

        # Block types
        if cell_state.type == Blocks.BRICK.value:
            pyxel.rect(x, y, self.dim, self.dim, pyxel.COLOR_BROWN)
        elif cell_state.type == Blocks.STONE.value:
            pyxel.rect(x, y, self.dim, self.dim, pyxel.COLOR_GRAY)
        elif cell_state.type == Blocks.MIRROR_NE.value:
            pyxel.line(x, y, x + self.dim, y + self.dim, pyxel.COLOR_YELLOW)
        elif cell_state.type == Blocks.MIRROR_SE.value:
            pyxel.line(x, y + self.dim, x + self.dim, y, pyxel.COLOR_YELLOW)

        self.tank.draw()
        self.enemies.draw()
        self.projectiles.draw()
        self.blocks.draw()

    def pre_draw_grid(self) -> None:
        pyxel.cls(0)
        pyxel.text(5, 5, f"Score: {self.score}", 7)


BattleCity().run(title="Battle City", fps=60)
