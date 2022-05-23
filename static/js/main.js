const console_ = document.querySelector('#console');
const spans = document.querySelectorAll('.textSpan');
let id_;
const enemyBtn = document.querySelector('#enemyBtn');
const playerBtn = document.querySelector('#playerBtn');
const saveBtn = document.getElementById('saveBtn');
const textBox = document.getElementById('user_text');
const resumeBtn = document.querySelector('#resumeBtn')
const alertBtn = document.querySelector('#alert_box')

function removeAllChildElements(ele){
    while(ele.firstChild){
        ele.removeChild(ele.firstChild)
    }
}

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
        socket.emit("move", {dx:0, dy:1});
    };

    var btn_w = document.getElementById("go_w");
    btn_w.onclick = function(e) {
        socket.emit("move", {dx:-1, dy:0, id: id_});
    };

    var btn_e = document.getElementById("go_e");
    btn_e.onclick = function(e) {
        socket.emit("move", {dx:1, dy:0});}

    playerBtn.onclick = function(e){
        e.preventDefault()
        socket.emit("add_player")
    }
    enemyBtn.onclick = function(e){
        e.preventDefault()
        socket.emit('add_enemy')
    }
    saveBtn.onclick = function(e){
        console.log("save button clicked")
        e.preventDefault();
        username = textBox.value
        socket.emit('save_game', username)
        alertBtn.innerHTML = `Saving game with username: ${username}`
        setTimeout(function(){
            alertBtn.innerHTML = ''
        }, 3000)
    }
    resumeBtn.onclick = function(e){
        e.preventDefault()
        username = textBox.value
        socket.emit("resume_game", username)
        alertBtn.innerHTML = `Resuming game with username: ${username}`
        setTimeout(function(){
            alertBtn.innerHTML = ''
        }, 3000)
    }
    //socket.on('login') enter the client id into a variable. Use it whenever moving / updating player

    socket.on("response", function(map){
/*         for( var i=0; i<2; i++){
            var cell_id = "cell " + data[i].i + "-" + data[i].j;
            var span_to_modif = document.getElementById(cell_id);
            span_to_modif.textContent = data[i].content;
            if(span_to_modif.innerHTML.includes('@')){
                span_to_modif.classList.add('btn');}
            else {
                span_to_modif.classList.remove('btn');}
        } */
        n = map.length
        m = map[0].length

        for(var i=0; i<n; i++){
            for(var j=0; j<m; j++){
                var cell_id = "cell " + i + "-" + j;
                clientSpan = document.getElementById(cell_id);
                removeAllChildElements(clientSpan)
                clientSpan.textContent=''
                clientSpan.style.backgroundColor = "white"
                if (map[i][j] == "@"){
                    im = document.createElement('img')
                    im.src = "../static/rogue_player.jpeg"
                    clientSpan.appendChild(im)
                    clientSpan.style.margin = "-4px"
                }
        
                else if (map[i][j] == "&"){
                    im2 = document.createElement('img');
                    im2.src = "../static/enemy.png"
                    clientSpan.appendChild(im2);
                    clientSpan.style.margin = "-7px"
                }
                else if (map[i][j] == "^"){
                    /* food ! */
                    im2 = document.createElement('img');
                    im2.src = "../static/banana.png"
                    clientSpan.appendChild(im2);
                    clientSpan.style.margin = "-2px"
                }
                else if (map[i][j] == "$"){
                    /* life ! */
                    im2 = document.createElement('img');
                    im2.src = "../static/heart.jpeg"
                    clientSpan.appendChild(im2);
                    clientSpan.style.margin = "-2px"
                }
                else if (map[i][j] == "!"){
                    /* sword ! */
                    im2 = document.createElement('img');
                    im2.src = "../static/sword.jpg"
                    clientSpan.appendChild(im2);
                    clientSpan.style.margin = "-1px"
                }
                else if (map[i][j] == "#"){
                    /* sword ! */
                    clientSpan.textContent='# ';
                    clientSpan.style.backgroundColor = "grey";
                }
                else{
                    clientSpan.textContent = map[i][j] + " ";
                    clientSpan.style.margin = "0px"
                }
            }
        }
    });
    socket.on("inventory", function(inventory){
        player_foods = document.getElementById('food_box');
        removeAllChildElements(player_foods)
        for(i = 0; i<inventory['food']; i++){
            img = document.createElement('img')
            img.src = "../static/banana.png"
            player_foods.appendChild(img)
            setTimeout(function(){
                player_foods.removeChild(player_foods.lastChild)
            }, 10000)
        }
        player_lifes = document.getElementById('life_box');
        removeAllChildElements(player_lifes)
        for(i = 0; i<inventory['life']; i++){
            img = document.createElement('img')
            img.src = "../static/heart.jpeg"
            player_lifes.appendChild(img)
        }
        player_weapons = document.getElementById('weapon_box');
        removeAllChildElements(player_weapons)
        for(i = 0; i<inventory['sword']; i++){
            img = document.createElement('img')
            img.src = "../static/sword.jpg"
            player_weapons.appendChild(img)
        }
        player_killcount = document.getElementById('killcount_box');
        removeAllChildElements(player_killcount);
        player_killcount.textContent = `Killcount: ${inventory['killcount']}`

        player_deathcount = document.getElementById('deathcount_box');
        removeAllChildElements(player_deathcount);
        player_deathcount.textContent = `Deathcount: ${inventory['deathcount']}`
    })



    socket.on("GameOver", function(){
        alertBtn.innerHTML = "Game Over! Respawning!"
        setTimeout(function(){
            alertBtn.innerHTML = ""
        }, 3000)
    })
/*     socket.on("response_enemies", function(enemies_data){
        for(let data of enemies_data){
            for(var i=0; i<2; i++){
                var cell_id = "cell " + data[i].i + "-" + data[i].j;
                var span_to_modif = document.getElementById(cell_id);
                span_to_modif.textContent = data[i].content;
            }
        }
    }); */
 
/*     setInterval(function(){
        socket.emit("move_enemies")
    }, 1000) */

});


/* add cool graphics */
