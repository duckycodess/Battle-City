import pyxel
from random import randint
class Block:
    def __init__(self, type: int = 0) -> None:
        self.type = type
        self.width = 16
        self.height = 16
        self.blocks = [(x, 60) for x in range(20, 240, 40)]
    
    def draw(self):
        for x, y in self.blocks:
            pyxel.rect(x, y, self.width, self.height, 10)