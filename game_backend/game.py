from operator import itemgetter
from .map_generator import Generator
from .player import Enemy, Player
from collections import namedtuple
import random
import numpy as np

Sprite =  namedtuple('Sprite', ['x','y', 'content'])

class Game:
    def __init__(self, width=64, height=32):
        self._generator = Generator(width=width, height=height)
        self._generator.gen_level()
        self._generator.gen_tiles_level()
        self._map = self._generator.tiles_level
        self._generator = Generator(width=width, height=height)
        self._generator.gen_level()
        self._generator.gen_tiles_level(2)
        self._map2 = self._generator.tiles_level2
        self.players = {}
        self.enemies = []
        self.sprites = []


    def move_player_sid(self, dx, dy, sid):
        return self.players[sid].move(dx, dy, self._map, self._map2)

    def add_my_player(self, sid):
        p = Player()
        try: 
            p.initPos(self._map)
        except: 
            raise Exception("Failure in init pos")
        self._map[p._y][p._x] = p.symbol
        self.players[sid] = p 
        p.sid = sid

    def add_enemy(self, level:int):
        if level == 1:
            _map = self._map
        if level ==2:
            _map = self._map2
        enemy = Enemy()
        enemy.init_pos(_map)
        _map[enemy._y][enemy._x] = enemy._symbol
        
    def move_enemies(self):
        for enemy in self.enemies:
            enemy.move_automatically(self._map)

    def add_item(self, level = 1):
        if level == 1:
            _map = self._map
        if level == 2:
            _map = self._map2
        items = ['^', '!', '$'] #food, sword, life
        i = np.random.randint(0,3)
        item_to_choose = items[i]

        y = random.randint(0,len(_map)-1)
        found = False
        while found == False:
            y = random.randint(0,len(_map)-1)
            tries = 0
            while True and tries<10: 
                x = random.randint(0,len(_map[0])-1)
                tries += 1
                if _map[y][x] == '.':
                    found = True
                    break
        if found:
            item_sprite = Sprite(x,y,item_to_choose)
            self.sprites.append(item_sprite)
            _map[item_sprite.y][item_sprite.x] = item_sprite.content
        else:
            self.add_item()





# fix levels, then work on saving