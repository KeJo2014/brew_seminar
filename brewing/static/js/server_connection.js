let url = `ws://${window.location.host}/ws/socket-server/`
 
        const chatSocket = new WebSocket(url)

        chatSocket.onmessage = function(e){
            let data = JSON.parse(JSON.parse(e.data).message);
            console.log(data);


                switch (data.command) {
                    case "update":
                        update_site(data)
                        if(data.status == "maischen"){
                            send_to_server("keep_maischen","")
                        }
                        else if(data.status == "warmingUp"){
                            send_to_server("keep_maischen","")
                        }
                        break;
                
                    default:
                        console.log("that command is unknown")
                        break;
                }
            
        }

        // let form = document.getElementById('form')
        // form.addEventListener('submit', (e)=> {
        //     e.preventDefault()
        //     let message = e.target.message.value 
        //     chatSocket.send(JSON.stringify({
        //         'message':message
        //     }))
        //     form.reset()
        // })

        function send_to_server(command, msg){
            if(msg == ""){
                text = {
                    'command':command,
                }
            }else{
                text = {
                    'command':command,
                    'message':msg
                }
            }
            chatSocket.send(JSON.stringify(text))
        }

        function update_site(data){
            //controll buttons
            if(data.status == "running"){
                document.getElementById("but-start").style.display = "none"
                document.getElementById("but-reset").style.display = "block"
            }else{
                document.getElementById("but-start").style.display = "block"
                document.getElementById("but-reset").style.display = "none"
            }
            // Data terminal
            let phase = document.getElementById("phase");
            let temperature = document.getElementById("temp");
            let engine = document.getElementById("engine");
            let duration = document.getElementById("duration");
            let finish_time = document.getElementById("finish_time");
            // steps
            let current_title = document.getElementById("currentPhase");
            let current_description = document.getElementById("currentContent");
            let next_title = document.getElementById("nextPhase");
            let next_description = document.getElementById("nextContent");
        
            //assign values terminal
            phase.innerHTML = data.step;
            temperature.innerHTML = data.sensor_data.temperature;
            if(data.sensor_data.engine_mode == true){
                engine.innerHTML = "ON";
            }else{
                engine.innerHTML = "OFF";
            }
            duration.innerHTML = "I don't know";
            finish_time.innerHTML = "Can we say that?";
            //assign values steps
            current_title.innerHTML = data.roadmap[0][data.step];
            current_description.innerHTML = data.roadmap[1][data.step];
            if(data.roadmap[0][data.step+1] != undefined){  
                next_title.innerHTML = data.roadmap[0][data.step+1];
                next_description.innerHTML = data.roadmap[1][data.step+1];
                document.getElementById("next_step_headline").style.display = "block";
            }else{
                next_title.innerHTML = "";
                next_description.innerHTML = "";
                document.getElementById("next_step_headline").style.display = "none";
            }
        }
        
function next(){
    send_to_server("next","")
}

function prev(){
    send_to_server("prev","")
}

function start(){
    send_to_server("start","")
}

function reset(){
    send_to_server("reset","")
}