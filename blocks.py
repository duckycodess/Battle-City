import pyxel
class Block:
    def __init__(self) -> None:
        self.width = 16
        self.height = 16
        self.blocks: list[tuple[int, int, int]] = []
        self.empty_blocks: list[tuple[int, int]] = []
        self.bg = 0
    
    def draw(self):
        for x, y, type in self.blocks:
            if type == 0:
                pass
            elif type == 1:
                pyxel.rect(x, y, self.width, self.width, self.bg)
                pyxel.blt(x, y, 0, 16, 48, 16, 16)
            elif type == 2:
                pyxel.rect(x, y, self.width, self.width, self.bg)
                pyxel.blt(x, y, 0, 0, 48, 16, 16)
            elif type == 3:
                pyxel.line(x, y, x+self.width, y+self.height, self.bg)
                pyxel.blt(x, y, 0, 0, 64, 16, 16)
            elif type == 4:
                pyxel.line(x, y, x+self.width, y+self.height, self.bg)
                pyxel.blt(x, y, 0, 16, 64, 16, 16)
            elif type == 5:
                pyxel.rect(x, y, self.width, self.width, self.bg)
                pyxel.blt(x, y, 0, 32, 48, 16, 16)
            elif type == 6:
                pyxel.rect(x, y, self.width, self.width, self.bg)
                pyxel.blt(x, y, 0, 48, 48, 16, 16)
            elif type == 8:
                pyxel.blt(x, y, 0, 48, 64, 16, 16)
            elif type == 9:
                pyxel.rect(x,y,self.width, self.width, 2)
    
    def draw_forest(self):
        for x, y, type in self.blocks:
            if type == 7:
                pyxel.blt(x, y, 0, 32, 64, 16, 16, 6)