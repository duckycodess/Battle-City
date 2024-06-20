import pyxel


class Enemies:
    def __init__(self) -> None:
        self.enemy_tank: list[tuple[tuple[int, int], str, str, int]] = [] # ((x,y), direction, enemy_id, type)
        self.width = 16
        self.height = 16
        self.bg = 0

    def update(self):
        pass
    def draw(self):
        for (x, y), direction, _, t in self.enemy_tank:
            if t == 0: #normal
                if direction == 'UP':
                    pyxel.rect(x, y, self.width, self.height, self.bg)
                    pyxel.blt(x, y, 0, 0, 16, 16, 16, 0)
                elif direction == 'DOWN':
                    pyxel.rect(x, y, self.width, self.height, self.bg)
                    pyxel.blt(x, y, 0, 16, 16, 16, 16, 0)
                elif direction == 'RIGHT':
                    pyxel.rect(x, y, self.height, self.width, self.bg)
                    pyxel.blt(x, y, 0, 32, 16, 16, 16, 0)
                elif direction == 'LEFT':
                    pyxel.rect(x, y, self.height, self.width, self.bg)
                    pyxel.blt(x, y, 0, 48, 16, 16, 16, 0)
            elif t == 1: #may shield
                if direction == 'UP':
                    pyxel.rect(x, y, self.width, self.height, self.bg)
                    pyxel.blt(x, y, 0, 0, 80, 16, 16, 0)
                elif direction == 'DOWN':
                    pyxel.rect(x, y, self.width, self.height, self.bg)
                    pyxel.blt(x, y, 0, 16, 80, 16, 16, 0)
                elif direction == 'RIGHT':
                    pyxel.rect(x, y, self.height, self.width, self.bg)
                    pyxel.blt(x, y, 0, 32, 80, 16, 16, 0)
                elif direction == 'LEFT':
                    pyxel.rect(x, y, self.height, self.width, self.bg)
                    pyxel.blt(x, y, 0, 48, 80, 16, 16, 0)
            elif t == 2: # walang shield
                if direction == 'UP':
                    pyxel.rect(x, y, self.width, self.height, self.bg)
                    pyxel.blt(x, y, 0, 0, 32, 16, 16, 0)
                elif direction == 'DOWN':
                    pyxel.rect(x, y, self.width, self.height, self.bg)
                    pyxel.blt(x, y, 0, 16, 32, 16, 16, 0)
                elif direction == 'RIGHT':
                    pyxel.rect(x, y, self.height, self.width, self.bg)
                    pyxel.blt(x, y, 0, 32, 32, 16, 16, 0)
                elif direction == 'LEFT':
                    pyxel.rect(x, y, self.height, self.width, self.bg)
                    pyxel.blt(x, y, 0, 48, 32, 16, 16, 0)