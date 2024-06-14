import pyxel

class Bullets:
    def __init__(self) -> None:
        self.bullets: list[tuple[int, int, int, int]] = []
        self.dir = "UP"
    
    def update(self):
        new_bullets: list[tuple[int, int, int, int]] = []
        for x, y, vx, vy in self.bullets:
            if 0 < x + vx < pyxel.width and 0 < y + vy < pyxel.height:
                new_bullets.append((x+vx, y+vy, vx, vy))
        self.bullets = new_bullets
    
    def draw(self):
        for x, y, _, _ in self.bullets:
            pyxel.circ(x, y, 1, 7)
    
    def fire(self, x: int, y: int, direction: str | None) -> None:
        bullets = self.bullets
        if direction == 'UP':
            bullets.append((x + 7, y, 0, -4))
        elif direction == 'DOWN':
            bullets.append((x + 7, y + 16, 0, 4))
        elif direction == 'LEFT':
            bullets.append((x, y + 7, -4, 0))
        elif direction == 'RIGHT':
            bullets.append((x + 16, y + 7, 4, 0))
        else:
            pass
