let url = `ws://${window.location.host}/ws/socket-server/`
 
        const chatSocket = new WebSocket(url)

        chatSocket.onmessage = function(e){
            let data = JSON.parse(e.data)
            

            if(data.type === 'chat'){
                let message = JSON.parse(data.message)
                switch (message.command) {
                    case "update":
                        update_site(message)
                        break;
                
                    default:
                        console.log("that command is unknown")
                        break;
                }
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

        function send_to_server(command){
            chatSocket.send(JSON.stringify({
            'message':command
        }))
        }

        function update_site(data){
            // Data terminal
            let phase = document.getElementById("phase");
            let temperature = document.getElementById("temp");
            let engine = document.getElementById("engine");
            let duration = document.getElementById("duration");
            let finish_time = document.getElementById("finish_time");
        
            //assign values
            phase.innerHTML = data.step;
            temperature.innerHTML = data.sensor_data.temperature;
            if(data.sensor_data.engine_mode == true){
                engine.innerHTML = "ON";
            }else{
                engine.innerHTML = "OFF";
            }
            duration.innerHTML = "I don't know";
            finish_time.innerHTML = "Can we say that?";
        }
        
