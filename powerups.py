import pyxel

class Powerup:
    def __init__(self) -> None:
        self.powerups: list[tuple[int, int, int]] = [] # [(x,y,type)]
        self.dim = 16
        self.timer = 0
        self.bg = 0

    def draw(self):
        for x,y,t in self.powerups:
            if t == 1:
                pyxel.rect(x, y, self.dim, self.dim, self.bg)
                pyxel.blt(x, y, 0, 32, 96, 16, 16, 6)
            elif t == 2:
                pyxel.rect(x, y, self.dim, self.dim, self.bg)
                pyxel.blt(x, y, 0, 48, 96, 16, 16, 6)
            elif t == 3:
                pyxel.rect(x, y, self.dim, self.dim, self.bg)
                pyxel.blt(x, y, 0, 16, 96, 16, 16, 6)