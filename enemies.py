import pyxel


class Enemies:
    def __init__(self) -> None:
        self.enemy_tank: list[tuple[tuple[int, int], str, str]] = [] # Enemy Placeholder location
        self.width = 16
        self.height = 16

    def update(self):
        pass
    def draw(self):
        for (x, y), direction, _ in self.enemy_tank:
            if direction == 'UP':
                pyxel.rect(x, y, self.width, self.height, 9)
                pyxel.blt(x, y, 0, 0, 16, 16, 16)
            elif direction == 'DOWN':
                pyxel.rect(x, y, self.width, self.height, 9)
                pyxel.blt(x, y, 0, 16, 16, 16, 16)
            elif direction == 'RIGHT':
                pyxel.rect(x, y, self.height, self.width, 9)
                pyxel.blt(x, y, 0, 32, 16, 16, 16)
            elif direction == 'LEFT':
                pyxel.rect(x, y, self.height, self.width, 9)
                pyxel.blt(x, y, 0, 48, 16, 16, 16)