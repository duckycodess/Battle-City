import pyxel
class Block:
    def __init__(self) -> None:
        self.width = 16
        self.height = 16
        self.blocks: list[tuple[int, int, int]] = []
    
    def draw(self):
        for x, y, type in self.blocks:
            if type == 0:
                pass
            elif type == 1:
                pyxel.rect(x, y, self.width, self.width, 0)
                pyxel.blt(x, y, 0, 16, 48, 16, 16)
            elif type == 2:
                pyxel.rect(x, y, self.width, self.width, 0)
                pyxel.blt(x, y, 0, 0, 48, 16, 16)
            elif type == 3:
                pyxel.line(x, y, x+self.width, y+self.height, 0)
                pyxel.blt(x, y, 0, 0, 64, 16, 16)
            elif type == 4:
                pyxel.line(x, y, x+self.width, y+self.height, 0)
                pyxel.blt(x, y, 0, 16, 64, 16, 16)
            elif type == 5:
                pyxel.rect(x, y, self.width, self.width, 0)
                pyxel.blt(x, y, 0, 32, 48, 16, 16)
            elif type == 6:
                pyxel.rect(x, y, self.width, self.width, 0)
                pyxel.blt(x, y, 0, 48, 48, 16, 16)
            elif type == 7:
                pyxel.blt(x, y, 0, 32,64, 16, 16, 6)
            elif type == 9:
                pyxel.rect(x,y,self.width, self.width, 2)