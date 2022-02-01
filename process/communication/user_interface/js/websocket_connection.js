//global variables
recipe = null

// Create WebSocket connection.
const socket = new WebSocket('ws://localhost:80');

// Connection opened
socket.addEventListener('open', function (event) {
    console.log('Connected to the WS Server!') 
});

// Connection closed
socket.addEventListener('close', function (event) {
    console.log('Disconnected from the WS Server!')
});

// Listen for messages
socket.addEventListener('message', function (event) {
    //console.log('Message from server', event.data);
    x = JSON.parse(event.data);
    switch (x['command']) {
        case 'next_server_step':
            console.log("server status update! mode: " + x['Server-Status']+ " || recipe progress: " + x['recipe-progress']);
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
            console.log(x);
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
function protocoll(){
    socket.send('{"command":"safe_protocol","protocol":"test"}');
}
function get_recipe(){
    socket.send('{"command":"get_recipe"}');
}

// get global variables
function get_recipe_content(){
    return recipe;
}