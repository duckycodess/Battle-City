import pyxel

class Tank:
    def __init__(self, x: int, y: int) -> None:
        self.player_x = x
        self.player_y = y
        self.direction = 'UP'
        self.height = 16
        self.width = 16
    
    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x = max(self.player_x - 2, 0)
            self.direction = 'LEFT'
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x = min(self.player_x + 2, pyxel.width - self.width)
            self.direction = 'RIGHT'
        elif pyxel.btn(pyxel.KEY_UP):
            self.player_y = max(self.player_y - 2, 0)
            self.direction = 'UP'
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.player_y = min(self.player_y + 2, pyxel.height - self.width)
            self.direction = 'DOWN'
        
    
    def draw(self):
        if self.direction == 'UP':
            pyxel.rect(self.player_x, self.player_y, self.width, self.height, 9)
            pyxel.blt(self.player_x, self.player_y, 0, 0, 0, 16, 16)
        elif self.direction == 'DOWN':
            pyxel.rect(self.player_x, self.player_y, self.width, self.height, 9)
            pyxel.blt(self.player_x, self.player_y, 0, 16, 0, 16, 16)
        elif self.direction == 'RIGHT':
            pyxel.rect(self.player_x, self.player_y, self.height, self.width, 9)
            pyxel.blt(self.player_x, self.player_y, 0, 32, 0, 16, 16)
        elif self.direction == 'LEFT':
            pyxel.rect(self.player_x, self.player_y, self.height, self.width, 9)
            pyxel.blt(self.player_x, self.player_y, 0, 48, 0, 16, 16)
