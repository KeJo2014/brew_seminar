//global variables
recipe = null
progress = 0;
temp = 0;
engine = "AUS";
logs = [];

// Create WebSocket connection.
const socket = new WebSocket('ws://localhost:80');

// Connection opened
socket.addEventListener('open', function (event) {
    console.log('Connected to the WS Server!') 
    get_recipe();
    get_step();
    get_logs_from_Server();
});

// Connection closed
socket.addEventListener('close', function (event) {
    console.log('Disconnected from the WS Server!')
});

// Listen for messages
socket.addEventListener('message', function (event) {
    //console.log('Message from server', event.data);
    x = JSON.parse(event.data);
    console.log(x);
    switch (x['command']) {
        case 'next_server_step':
            console.log("server status update! mode: " + x['Server-Status']+ " || recipe progress: " + x['recipe-progress']);
            get_step();
            break;
        case 'select_recipe':
            console.log("test.fbp seems to be selected");
            socket.send('{"command":"select_recipe","response":"test.fbp"}');
            break;
        case 'finish_maisch':
            console.log('finish_maisch! | sending next step');
            socket.send('{"command":"next"}');
            break;
        case 'reponse':
            console.log("Server response: " + x);
            break;
        case 'error':
            console.log("Server error: " + x['error_msg']);
            break;
        case 'step':
            console.log(x["response"]["recipe-progress"]);
            progress = x["response"]["recipe-progress"];
            update_interface();
            break;
        case 'logs':
            logs = x['response'];
            console.log(x)
            break;
        case 'switch_to_maischen':
            console.log("Switch to Maische");
            socket.send('{"command":"switch_to_maischen"}');
            break;
        case 'm_update':
            console.log(x);
            break;
        case 'recipe_content':
            recipe = x['response'];
            console.log("recipe received from server");
            break;
        case 'transmit_information':
            temp = x['m_temp'];
            if(x['m_engine'] == "false"){
                engine = "AUS";
            }else{
                engine = "EIN";
            }
            update_interface();
            break;
        default:
            console.log("Unkown command: " + event.data);

            break;
    }
});
// Send a msg to the websocket
function start(){
    socket.send('{"command":"start"}');
}
function next(){
    socket.send('{"command":"next"}');
}
function reset(){
    socket.send('{"command":"reset"}');
}
function undo(){
    socket.send('{"command":"undo_last"}');
}
function stop(){
    socket.send('{"command":"stop"}');
}
function protocol(){
    socket.send('{"command":"safe_protocol","protocol":"test"}');
}
function get_logs_from_Server(){
    socket.send('{"command":"get_logs"}');
}
function get_recipe(){
    socket.send('{"command":"get_recipe"}');
}
function get_step(){
    socket.send('{"command":"get_step"}');
}

// get global variables
function get_recipe_content(){
    return recipe;
}
function get_step_number(){
    return progress;
}
function get_temp(){
    return temp;
}
function get_engine(){
    return engine;
}
function get_logs(){
    return logs;
}