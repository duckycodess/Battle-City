import pyxel

class Bullets:
    def __init__(self) -> None:
        self.bullets: dict[str, list[tuple[int, int, int, int]]] = {
            "player": [],
            # Enemy bullets will be stored with keys like "enemy_1", "enemy_2", etc.
        }
    
    def update(self):
        new_bullets: dict[str, list[tuple[int, int, int, int]]] = {}
        for owner, bullet_list in self.bullets.items():
            new_bullets[owner] = []
            for x, y, vx, vy in bullet_list:
                if 0 < x + vx < pyxel.width and 0 < y + vy < pyxel.height:
                    new_bullets[owner].append((x + vx, y + vy, vx, vy))
        self.bullets = new_bullets
    
    def draw(self):
        for owner, bullet_list in self.bullets.items():
            color = 9 if owner == "player" else 8
            for x, y, _, _ in bullet_list:
                pyxel.circ(x, y, 1, color)
    
    def fire(self, owner: str, x: int, y: int, direction: str) -> None:
        if owner not in self.bullets:
            self.bullets[owner] = []

        if direction == 'UP':
            self.bullets[owner].append((x + 7, y, 0, -4))
        elif direction == 'DOWN':
            self.bullets[owner].append((x + 7, y + 16, 0, 4))
        elif direction == 'LEFT':
            self.bullets[owner].append((x, y + 7, -4, 0))
        elif direction == 'RIGHT':
            self.bullets[owner].append((x + 16, y + 7, 4, 0))
    
    def check_collision(self, player_key: str, enemy_keys: list[str]):
        new_player_bullets: list[tuple[int, int, int, int]] = []
        for bx, by, vx, vy in self.bullets[player_key]:
            hit = False
            for enemy_key in enemy_keys:
                enemy_bullets = self.bullets.get(enemy_key, [])
                for ox, oy, _, _ in enemy_bullets:
                    if bx == ox and by == oy:
                        hit = True
                        break
                if hit:
                    break
            if not hit:
                new_player_bullets.append((bx, by, vx, vy))
        self.bullets[player_key] = new_player_bullets

        for enemy_key in enemy_keys:
            new_enemy_bullets: list[tuple[int, int, int, int]] = []
            for ox, oy, ovx, ovy in self.bullets.get(enemy_key, []):
                hit = False
                for bx, by, _, _ in self.bullets[player_key]:
                    if ox == bx and oy == by:
                        hit = True
                        break
                if not hit:
                    new_enemy_bullets.append((ox, oy, ovx, ovy))
            self.bullets[enemy_key] = new_enemy_bullets
