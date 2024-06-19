import pyxel

class Bullets:
    def __init__(self) -> None:
        self.bullets: dict[str, list[tuple[int, int, int, int]]] = {
            "player": [],
            # Enemy bullets will be stored with keys like "enemy_1", "enemy_2", etc.
        }
        self.r = 1
        self.velocity = 3
    
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
            color = 8 if owner == "player" else 9
            for x, y, _, _ in bullet_list:
                pyxel.circ(x, y, self.r, color)
    
    def fire(self, owner: str, x: int, y: int, direction: str) -> None:
        if owner not in self.bullets:
            self.bullets[owner] = []

        if direction == 'UP':
            self.bullets[owner].append((x+7, y + 3, 0, -self.velocity))
        elif direction == 'DOWN':
            self.bullets[owner].append((x + 8, y + 13, 0, self.velocity))
        elif direction == 'LEFT':
            self.bullets[owner].append((x + 3, y + 7, -self.velocity, 0))
        elif direction == 'RIGHT':
            self.bullets[owner].append((x + 13, y + 7, self.velocity, 0))
    
    def check_collision(self, player_key: str, enemy_keys: list[str]):
        new_player_bullets: list[tuple[int, int, int, int]] = []
        for bx, by, vx, vy in self.bullets[player_key]:
            hit = False
            for enemy_key in enemy_keys:
                enemy_bullets = self.bullets.get(enemy_key, [])
                for ox, oy, _, _ in enemy_bullets:
                    if (ox-self.r <= bx <= ox+self.r and oy-self.r <= by <= oy+self.r) or \
                        (bx-self.r <= ox <= bx+self.r and by-self.r <= oy <= by+self.r):
                        hit = True
                        self.bullets[enemy_key] = [e for e in enemy_bullets if not (e[0] == ox and e[1] == oy)]
                        break
                if hit:
                    break
            if not hit:
                new_player_bullets.append((bx, by, vx, vy))
        self.bullets[player_key] = new_player_bullets

        # enemy bullet destroy another enemy bullet when collided
        for i, enemy_key in enumerate(enemy_keys):
            new_enemy_bullets: list[tuple[int, int, int, int]] = []
            for ox, oy, ovx, ovy in self.bullets.get(enemy_key, []):
                hit2 = False
                for other_enemy_key in enemy_keys[i+1:]:
                    other_enemy_bullets = self.bullets.get(other_enemy_key, [])
                    for o2x, o2y, _, _ in other_enemy_bullets:
                        if (o2x - self.r <= ox <= o2x + self.r and o2y - self.r <= oy <= o2y + self.r) or \
                            (ox - self.r <= o2x <= ox + self.r and ox - self.r <= o2y <= oy + self.r):
                            hit2 = True
                            self.bullets[other_enemy_key] = [b for b in other_enemy_bullets if not (b[0] == o2x and b[1] == o2y)]
                            break
                    if hit2:
                        break
                if not hit2:
                    new_enemy_bullets.append((ox, oy, ovx, ovy))
            self.bullets[enemy_key] = new_enemy_bullets