const console_ = document.querySelector('#console');
const spans = document.querySelectorAll('.textSpan');
let id_;
const enemyBtn = document.querySelector('#enemyBtn');
const playerBtn = document.querySelector('#playerBtn');

window.addEventListener("DOMContentLoaded", (event) => {
    var socket = io.connect("http://" + document.domain + ":" + location.port );
    for(let span of spans){
        if(span.innerHTML.includes("#")){
            span.style.backgroundColor = 'grey'
        }
    }
    document.onkeydown = function(e){
        console.log('key down pressed, move message emitted')
        switch(e.keyCode){
            case 37:
                socket.emit("move", {dx:-1, dy:0});
                break;
            case 38:
                socket.emit("move", {dx:0, dy:-1});
                break;
            case 39:
                socket.emit("move", {dx:1, dy:0});
                break;
            case 40:
                socket.emit("move", {dx:0, dy:1});
                break;
        }


    };
    
    var btn_n = document.getElementById("go_n");
    btn_n.onclick = function(e) {
        console.log("Clicked on button north");
        socket.emit("move", {dx:0, dy:-1});
    };

    var btn_s = document.getElementById("go_s");
    btn_s.onclick = function(e) {
        console.log("Clicked on button south");
        socket.emit("move", {dx:0, dy:1});
    };

    var btn_w = document.getElementById("go_w");
    btn_w.onclick = function(e) {
        console.log("Clicked on button w");
        socket.emit("move", {dx:-1, dy:0, id: id_});
    };

    var btn_e = document.getElementById("go_e");
    btn_e.onclick = function(e) {
        console.log("Clicked on button e");
        socket.emit("move", {dx:1, dy:0});}

    playerBtn.onclick = function(e){
        console.log("clicked on button playerBtn");
        e.preventDefault()
        socket.emit("add_player")
    }
    enemyBtn.onclick = function(e){
        console.log("clicked on btn enemyBtn");
        e.preventDefault()
        socket.emit('add_enemy')
    }
    //socket.on('login') enter the client id into a variable. Use it whenever moving / updating player

    socket.on("response", function(data){
        console.log(data);
        for( var i=0; i<2; i++){
            var cell_id = "cell " + data[i].i + "-" + data[i].j;
            var span_to_modif = document.getElementById(cell_id);
            span_to_modif.textContent = data[i].content;
            if(span_to_modif.innerHTML.includes('@')){
                span_to_modif.classList.add('btn');}
            else {
                span_to_modif.classList.remove('btn');}
        }
    });
    socket.on("response_enemies", function(enemies_data){
        for(let data of enemies_data){
            for(var i=0; i<2; i++){
                var cell_id = "cell " + data[i].i + "-" + data[i].j;
                var span_to_modif = document.getElementById(cell_id);
                span_to_modif.textContent = data[i].content;
            }
        }
    });
 
    setInterval(function(){
        socket.emit("move_enemies")
    }, 5000)

});


/* add cool graphics */
