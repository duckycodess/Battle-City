import pyxel
import random

class Tank:
    def __init__(self, x: int, y: int) -> None:
        self.player_x = x
        self.player_y = y
        self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        self.height = 16
        self.width = 16
        self.speed = 2
        self.is_block_colliding:bool = False
        self.move_x, self.move_y = self.player_x, self.player_y
        self.dim = 18
        self.gatling_mode = False
        self.powerup_timer = 0
        self.invincibility_mode = False
        self.bg = 0
    
    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            self.move_x = max(self.player_x - self.speed, 0)
            self.direction = 'LEFT'
        elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.move_x = min(self.player_x + self.speed, pyxel.width - self.width)
            self.direction = 'RIGHT'
        elif pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
            self.move_y = max(self.player_y - self.speed, 0)
            self.direction = 'UP'
        elif pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            self.move_y = min(self.player_y + self.speed, pyxel.height - self.width)
            self.direction = 'DOWN'

        # GATLING mode
        if self.gatling_mode:
            self.powerup_timer -= 1
            if self.powerup_timer <= 0:
                self.gatling_mode = False
        
        # INVINCIBILITY mode
        if self.invincibility_mode:
            self.powerup_timer -= 1
            if self.powerup_timer <= 0:
                self.gatling_mode = False
    
    def draw(self):
        if self.direction == 'UP':
            pyxel.rect(self.player_x, self.player_y, self.width, self.height, self.bg)
            pyxel.blt(self.player_x, self.player_y, 0, 0, 0, 16, 16, 0)
        elif self.direction == 'DOWN':
            pyxel.rect(self.player_x, self.player_y, self.width, self.height, self.bg)
            pyxel.blt(self.player_x, self.player_y, 0, 16, 0, 16, 16, 0)
        elif self.direction == 'RIGHT':
            pyxel.rect(self.player_x, self.player_y, self.height, self.width, self.bg)
            pyxel.blt(self.player_x, self.player_y, 0, 32, 0, 16, 16, 0)
        elif self.direction == 'LEFT':
            pyxel.rect(self.player_x, self.player_y, self.height, self.width, self.bg)
            pyxel.blt(self.player_x, self.player_y, 0, 48, 0, 16, 16, 0)

    def activate_gatling(self, duration: int):
        self.gatling_mode = True
        self.powerup_timer = duration
    
    def activate_invincibility(self, duration: int):
        self.invincibility_mode = True
        self.powerup_timer = duration


