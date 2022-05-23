from flask import Flask, render_template, request, flash, session
from flask_socketio import SocketIO
from game_backend import Game
from flask_sqlalchemy import SQLAlchemy
import json

from game_backend.player import Player

app = Flask(__name__)
socketio = SocketIO(app)
game = Game()
app.config['SECRET_KEY'] = "hello there my name is Tanguy"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///memory.db'
db = SQLAlchemy(app)


for k in range(20):
    game.add_item(level = 1)
    game.add_item(level = 2)


class User(db.Model):
    username = db.Column(db.String(80), primary_key = True, unique = True, nullable = False)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    level = db.Column(db.Integer)
    inventory = db.Column(db.String, unique = False, nullable = False)
    map = db.Column(db.String, unique = False, nullable = False)
    map2 = db.Column(db.String, unique = False, nullable = False) 
    def __repr__(self):
        return '<User %r>' % self.username
db.create_all()
def make_user(username,_x,_y,inventory,_map,_map2, level):
    assert(type(username) == str)
    if(type(_map) == list):
        _map = json.dumps(_map)
    if(type(_map2) == list):
        _map2 = json.dumps(_map2)
    if(type(inventory) != str):
        inventory = json.dumps(inventory)
    if User.query.get(username):
        user = User.query.get(username)
        print(f"updating user {user} in db.session")
        user.x = _x
        user.y = _y
        user.inventory = inventory
        user.map = _map
        user.map2 = _map2
    else:
        user = User(username = username, x = _x, y = _y, inventory = inventory, map = _map, map2 = _map2, level = level)
        print(f"adding user {user} to db.session")
        db.session.add(user)
    db.session.commit()

def get_user(username,game:Game,sid: str):
    game.sids[username] = sid
    player = Player()
    user = User.query.get(username)
    player._x = user.x
    player._y = user.y
    player.inventory = json.loads(user.inventory)
    l = user.level
    game._map = json.loads(user.map)
    game._map2 = json.loads(user.map2)
    if int(l) == 1:
        game._map[player._y][player._x] = player._symbol
    if int(l) == 2:
        game._map2[player._y][player._x] = player._symbol
    game.players[sid] = player

#creating all databases
db.create_all()

""" @app.route("/",methods = ['GET','POST'])
@app.route("/home", methods = ['GET','POST'])
def index():
    global map
    if request.method == "GET":
        return render_template("index.html", mapdata=map, n_row=len(map), n_col=len(map[0]) )
    if request.method == "POST":
        print("POST METHOD")
        if "enemy" in request.form:
            flash("You have added an enemy")
            game.add_enemy()
        if "player" in request.form:
            flash("You have added a player")
            game.add_my_player()
            socketio.emit("player_added", len(game.players)-1)
        return render_template("index.html", mapdata=map, n_row=len(map), n_col=len(map[0]) )
 """


@app.route("/")
@app.route("/home")
def index():
    level = 1
    if request.method == "GET" and level == 1 :
        return render_template("index.html", mapdata=game._map, n_row=len(game._map), n_col=len(game._map[0]) )
    if request.method == "GET" and level == 2 :
        return render_template("index.html", mapdata=game._map2, n_row=len(game._map), n_col=len(game._map[0]) )





@socketio.on('add_enemy')
def add_enemy():
    sid = request.sid
    p = game.players[sid]
    game.add_enemy(p.level)

@socketio.on('add_player')
def add_player():
    sid = request.sid
    print(f"ADD PLAYER FUNCTION----sid: {sid}")
    game.add_my_player(sid)


@socketio.on("move")
def on_move_msg(json):
    print(request.sid)
    sid = request.sid
    dx = json['dx']
    dy = json["dy"]
    survive, survive2, sid2 = game.move_player_sid(dx,dy, sid)
    if not survive:
        print(f"RESPAWNING MY PLAYER")
        game.respawn_player(sid)
    if survive2 == False and sid2:
        print(f"SECOND PLAYER DEAD")
        game.respawn_player(sid2)



@socketio.on("move_enemies")
def on_move_enemy_msg():
    game.move_enemies()

@socketio.on("show_id")
def on_show_id_msg(json):
    print(json)

#can i use pickle to go faster? 
@socketio.on("save_game")
def on_savegame_msg(data):
    print(f"saving game for user {data} with sid {request.sid}")
    game.sids[data] = request.sid
    try:
        player = game.players[request.sid]
    except KeyError as ke:
        print("You must choose a player")
        return
    inventory = player.inventory
    username = data
    make_user(username, player._x, player._y, inventory, game._map, game._map2, player.level)

@socketio.on("resume_game")
def on_resumegame_msg(data):
    print(f"resuming game for user {data} with sid {request.sid}")
    get_user(data,game,request.sid)
    

#refresh with a timer thread
import threading, time
def refresh():
    while True: 
        for sid, p in game.players.items():
            if p.level == 1:
                socketio.emit("response", game._map, to = sid )
            if p.level == 2:
                socketio.emit("response", game._map2, to = sid )
            socketio.emit('inventory', p.inventory, to = sid)
        time.sleep(1/5)
t = threading.Thread(target=refresh, args = ())
t.start()



if __name__=="__main__":
    socketio.run(app, port=5001, debug=True)


