from flask import Flask, render_template, request, flash
from flask_socketio import SocketIO
from game_backend import Game

app = Flask(__name__)
socketio = SocketIO(app)
game = Game()
app.config['SECRET_KEY'] = "hello there my name is Tanguy"
map = game.getMap()



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
    global map
    if request.method == "GET":
        return render_template("index.html", mapdata=map, n_row=len(map), n_col=len(map[0]) )

@socketio.on('add_enemy')
def add_enemy():
    flash("You have added an enemy")
    game.add_enemy()

@socketio.on('add_player')
def add_player():
    sid = request.sid
    flash("You have added a player")
    game.add_my_player(sid)

@socketio.on("move")
def on_move_msg(json):
    print(request.sid)
    sid = request.sid
    print(json)
    print("received move message")
    dx = json['dx']
    dy = json["dy"]
    data, survive = game.move_player_sid(dx,dy, sid)
    if survive and data:
        socketio.emit("response", data)
    if not survive:
        del game.players[sid]
    if not data: #do not move player
        pass


@socketio.on("move_enemies")
def on_move_enemy_msg():
    print("received move enemy message")
    flash("received move_enemies")
    all_enemies_data = game.move_enemies()
    socketio.emit("response_enemies", all_enemies_data)

@socketio.on("show_id")
def on_show_id_msg(json):
    flash("received show_id in app.py")
    print(json)

if __name__=="__main__":
    socketio.run(app, port=5001, debug=True)


