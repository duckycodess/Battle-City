import pyxel

class Enemies:
    def __init__(self) -> None:
        self.enemy_tank: list[tuple[int, int]] = [(200, 200)] # Enemy Placeholder location

    def update(self):
        pass
    
    def draw(self):
        for x, y in self.enemy_tank:
            pyxel.rect(x, y, 16, 8, 2)
            pyxel.blt(x, y, 0, 0, 0, 16, 16)
