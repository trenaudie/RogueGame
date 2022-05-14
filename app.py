from flask import Flask, render_template, request, flash, session
from flask_socketio import SocketIO
from game_backend import Game

app = Flask(__name__)
socketio = SocketIO(app)
game = Game()
app.config['SECRET_KEY'] = "hello there my name is Tanguy"
for k in range(20):
    game.add_item(level = 1)
    game.add_item(level = 2)



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
    print(json)
    print("received move message")
    dx = json['dx']
    dy = json["dy"]
    survive = game.move_player_sid(dx,dy, sid)
    inventory = game.players[sid].inventory
    if not survive:
        del game.players[sid]



@socketio.on("move_enemies")
def on_move_enemy_msg():
    print("received move enemy message")
    game.move_enemies()
    socketio.emit("response", game._map)

@socketio.on("show_id")
def on_show_id_msg(json):
    print(json)

#refresh with a timer thread
import threading, time
def refresh():
    print('REFRESH STARTED')
    while True: 
        for p in game.players.values():
            if p.level == 1:
                socketio.emit("response", game._map, to = p.sid )
            if p.level == 2:
                socketio.emit("response", game._map2, to = p.sid )
                print(game._map2[0][10:20])
            socketio.emit('inventory', p.inventory, to = p.sid)
        time.sleep(1/30)
t = threading.Thread(target=refresh, args = ())
t.start()



if __name__=="__main__":
    socketio.run(app, port=5001, debug=True)


