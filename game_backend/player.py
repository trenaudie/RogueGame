

import random


class Player:
    def __init__(self, symbol="@"):
        self._symbol = symbol
        self._x = None
        self._y = None

    def initPos(self, _map):
        n_row = len(_map)
        #n_col = len(_map[0])

        y_init = random.randint(0,n_row)
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

        _map[self._y][self._x] = self._symbol

    def move(self, dx, dy, map):
        new_x = self._x + dx
        new_y = self._y + dy

        if map[new_y][new_x] == ".":
            survive =True
            map[new_y][new_x] = self._symbol
            map[self._y][self._x] = "."
            data = [{"i": f"{self._y}", "j":f"{self._x}", "content":"."}, {"i": f"{new_y}", "j":f"{new_x}", "content":self._symbol}]
            self._x = new_x
            self._y = new_y
        if map[new_y][new_x] == "&":
            survive = False 
            map[self._y][self._x] = "."
        else:
            survive = True #player still alive 
            data = []
        return data, survive

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
        _map[self._y][self._x] = self._symbol

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
        data = [{"i": f"{self._y}", "j":f"{self._x}", "content":"."}, {"i": f"{new_y}", "j":f"{new_x}", "content":self._symbol}]
        self._x = new_x
        self._y = new_y
        return data
    

    


        
    

