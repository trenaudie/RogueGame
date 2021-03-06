

import random
import threading
import time 


class Player:
    def __init__(self, symbol="@"):
        self._symbol = symbol
        self.symbol = symbol
        self._x = None
        self._y = None
        self.level = 1
        self.inventory = {'sword' : 0, 'life' : 0, 'killcount': 0, 'food' : 0, 'deathcount':0}
        self.speed = 1

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
            print(f"new y:{self._y}")
        else:
            self.initPos(_map)


    def move(self, dx, dy, map, map2, enemylist, playerlist = None):
        survive2 = True
        sid2 = None
        if self.level == 1:
            main_map = map
            scnd_map = map2 
        if self.level == 2:
            main_map = map2
            scnd_map = map
        new_x = self._x + self.speed*dx
        new_y = self._y + self.speed*dy
        if new_x == -1 and new_y == len(map)//2:
            if self.level == 1:
                print("changing level to 2")
                self.level = 2
            elif self.level == 2:
                self.level = 1
            main_map[self._y][self._x] = '.'
            self._x = 2
            self._y = len(map)//2
            scnd_map[self._y][self._x] = '@'
            print(f'now self.level is equal to {self.level}')
            survive = True
        elif main_map[new_y][new_x] == ".":
            survive =True
            main_map[new_y][new_x] = self._symbol
            main_map[self._y][self._x] = "."
            self._x = new_x
            self._y = new_y
            main_map[self._y][self._x] = self.symbol
        elif main_map[new_y][new_x] == "&":
            print("ENEMY ENCOUNTERED")
            for enemy in enemylist:
                if (enemy._x, enemy._y, enemy.level) == (new_x,new_y,self.level):
                    enemy_found = enemy
            if self.inventory['sword'] >=1:
                print('ENEMY KILLED')
                survive = True
                main_map[self._y][self._x] = "."
                self._x = new_x
                self._y = new_y
                main_map[self._y][self._x] = self.symbol
                self.inventory['sword'] -= 1
                self.inventory['killcount'] += 1
                enemylist.remove(enemy_found)

            elif self.inventory['life'] >=1:
                print("LOST A LIFE")
                survive= True
                self.inventory['life'] -=1
                main_map[self._y][self._x] = "."
                self._x = new_x
                self._y = new_y
                main_map[self._y][self._x] = self.symbol
            
            else:
                print("PLAYER DEAD.")
                survive = False
                self.inventory['deathcount'] += 1
                main_map[self._y][self._x] = "."
                return False, True, None


        elif main_map[new_y][new_x] == "@":
            #find enemy in enemylist
            for p in playerlist:
                if (p._x, p._y, p.level) == (new_x,new_y,self.level):
                    player_found = p
                    sid2 = p.sid
            #if I have a sword
            if self.inventory['sword'] >=1:
                survive = True
                self.inventory['sword'] -= 1
                if player_found.inventory['life'] < 1: 
                    #player_found is dead
                    self.inventory['killcount'] += 1
                    player_found.inventory['deathcount'] += 1
                    main_map[new_y][new_x] = "."
                    survive2 = False
                else:
                    player_found.inventory['life'] -= 1
            #if other player has a sword
            if player_found.inventory['sword'] >=1:
                player_found.inventory['sword'] -= 1
                if self.inventory['life'] < 1: 
                    #I am dead
                    survive = False
                    self.inventory['deathcount'] += 1
                    player_found.inventory['killcount'] += 1
                    main_map[self._y][self._x] = "."
                else:
                    player_found.inventory['life'] -= 1

        elif main_map[new_y][new_x] == "!":
            survive = True
            self.inventory['sword'] += 1
            main_map[self._y][self._x] = "."
            self._x = new_x
            self._y = new_y
            main_map[self._y][self._x] = self.symbol
        elif main_map[new_y][new_x] == "$":
            survive = True
            self.inventory['life'] += 1
            main_map[self._y][self._x] = "."
            self._x = new_x
            self._y = new_y
            main_map[self._y][self._x] = self.symbol
        elif main_map[new_y][new_x] == "^":
            #banana eaten -> speed 
            survive = True
            self.inventory['food'] += 1
            main_map[self._y][self._x] = "."
            self._x = new_x
            self._y = new_y
            main_map[self._y][self._x] = self.symbol
            self.speed *= 2
            def change_speed(self):
                time.sleep(10)
                print("changing speed back to 1")
                self.speed = 1
                self.inventory['food'] -= 1
            t = threading.Thread(target = change_speed, args = (self,))
            t.start()
        else:
            survive = True #player still alive 
        return survive, survive2, sid2

class Enemy:
    def __init__(self, symbol="&"):
        self._symbol = symbol
        self._x = None
        self._y = None
        self.dx = 1,1
    
    def init_pos(self, _map, level : int):
        self.level = level
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
            self._x = x
            self._y = y
        else:
            self.init_pos(_map)


    def move_automatically(self, _map):
        dx = random.randint(-1,1),random.randint(-1,1)
        new_x = self._x + dx[0]
        new_y = self._y + dx[1]

        contained = False
        while contained is False: 
            if dx == self.dx: 
                dx = random.randint(-1,1),random.randint(-1,1)
                new_x = self._x + dx[0]
                new_y = self._y + dx[1]
                continue
            if _map[new_y][new_x] != '#':
                contained = True
            else: #you have hit a wall
                dx = random.randint(-1,1),random.randint(-1,1)
                new_x = self._x + dx[0]
                new_y = self._y + dx[1]
        if _map[new_y][new_x] == '@':
            print("GAMEOVER")
        _map[new_y][new_x] = self._symbol
        _map[self._y][self._x] = "."
        self._x = new_x
        self._y = new_y
    

    


        
    

