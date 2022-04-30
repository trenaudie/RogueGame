from .map_generator import Generator
from .player import Enemy, Player


class Game:
    def __init__(self, width=64, height=32):
        self._generator = Generator(width=width, height=height)
        self._generator.gen_level()
        self._generator.gen_tiles_level()
        self._map = self._generator.tiles_level
        self.players = {}
        self.enemies = []

    def getMap(self):
        return self._map

    def move_player_sid(self, dx, dy, sid):
        return self.players[sid].move(dx, dy, self._map)

    def add_my_player(self, sid):
        p = Player()
        p.initPos(self._map)
        self.players[sid] = p 

    def add_enemy(self):
        enemy = Enemy()
        enemy.init_pos(self._map)
        self.enemies.append(enemy)
        self._map[enemy._y][enemy._x] = enemy._symbol
        
    def move_enemies(self):
        all_enemies_data = []
        for enemy in self.enemies:
            data = enemy.move_automatically(self._map)
            all_enemies_data.append(data)
        return all_enemies_data



# [{"i": f"{self._y}", "j":f"{self._x}", "content":"."}, {"i": f"{new_y}", "j":f"{new_x}", "content":self._symbol}]    