

import random
import threading
import time 


class Player:
    def __init__(self, symbol="@"):
        self._symbol = symbol
        self._x = None
        self._y = None
        self.level = 1
        self.inventory = {'sword' : 0, 'life' : 0, 'killcount': 0, 'food' : 0}
        self.speed = 1
        self.symbol = "@"

    def initPos(self, _map):
        n_row = len(_map)
        #n_col = len(_map[0])

        y_init = random.randint(0,n_row)
        found = False
        while found is False:
            y_init += 1
            if y_init >= n_row:
                break
            for i,c in enumerate(_map[y_init]):
                if c == ".":
                    x_init = i
                    found = True
                    break
        if found:
            self._x = x_init
            self._y = y_init
        else:
            self.initPos(_map)


    def move(self, dx, dy, map):
        new_x = self._x + self.speed*dx
        new_y = self._y + self.speed*dy
        new_map = map[new_y][new_x]
        print("MOVE MESSAGE RESULT:")
        print("BEFORE:", new_map)
        if new_x == 0 and new_y == len(map)//2:
            print("you have reached a new level")
            self.level = 2
            return True
        if new_map == ".":
            survive =True
            new_map = self._symbol
            map[self._y][self._x] = "."
            self._x = new_x
            self._y = new_y
        elif new_map == "&":
            if self.inventory['sword'] >=1:
                survive = True
                map[self._y][self._x] = "."
                new_map = self._symbol
                self._x = new_x
                self._y = new_y
                self.inventory['sword'] -= 1
            if self.inventory['life'] >=1:
                survive= True
                self.inventory['life'] -=1
        elif new_map == "!":
            survive = True
            self.inventory['sword'] += 3
            map[self._y][self._x] = "."
            new_map = self.symbol
            self._x = new_x
            self._y = new_y
        elif new_map == "$":
            survive = True
            self.inventory['life'] += 1
            map[self._y][self._x] = "."
            new_map = self.symbol
            self._x = new_x
            self._y = new_y
        elif new_map == "^":
            survive = True
            self.inventory['food'] += 1
            map[self._y][self._x] = "."
            new_map = self.symbol
            self._x = new_x
            self._y = new_y
            self.speed *= 2
            def change_speed(self):
                time.sleep(5000)
                self.speed = 1
            t = threading.Thread(target = change_speed, args = (self,))
            t.start()
        else:
            survive = True #player still alive 
        return survive

class Enemy:
    def __init__(self, symbol="&"):
        self._symbol = symbol
        self._x = None
        self._y = None
    
    def init_pos(self, _map):
        n_row = len(_map)
        #n_col = len(_map[0])

        y_init = random.randint(1,n_row-1)
        found = False
        while found is False:
            y_init += 1
            for i,c in enumerate(_map[y_init]):
                if c == ".":
                    x_init = i
                    found = True
                    break

        self._x = x_init
        self._y = y_init

    def move_automatically(self, _map):
        new_x = self._x + random.randint(-1,1)
        new_y = self._y + random.randint(-1,1)

        contained = False
        while contained is False: 
            if _map[new_y][new_x] != '#':
                contained = True
            else: #you have hit a wall
                new_x = self._x + random.randint(-1,1)
                new_y = self._y + random.randint(-1,1)
        if _map[new_y][new_x] == '@':
            print("GAMEOVER")
        _map[new_y][new_x] = self._symbol
        _map[self._y][self._x] = "."
        self._x = new_x
        self._y = new_y
    

    


        
    

