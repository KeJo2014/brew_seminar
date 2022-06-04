let url = `ws://${window.location.host}/ws/socket-server/`
mode = false
count = 0;
createGraph()
showGraph(false);

const chatSocket = new WebSocket(url)

chatSocket.onmessage = function (e) {
    let data = JSON.parse(JSON.parse(e.data).message);
    console.log(data);


    switch (data.command) {
        case "update":
            update_site(data)
            if (data.status == "warmingUp") {
                send_to_server("keep_process", "")
                console.warn("AUFHEIZEN")
            }
            else if (data.status == "maischen" | data.status == "cooking") {
                send_to_server("keep_process", "")
            }
            break;

        default:
            console.log("that command is unknown")
            console.log(data)
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

function send_to_server(command, msg) {
    if (msg == "") {
        text = {
            'command': command,
        }
    } else {
        text = {
            'command': command,
            'message': msg
        }
    }
    chatSocket.send(JSON.stringify(text))
}

function update_site(data) {
    //controll buttons
    if (data.status != "waiting") {
        document.getElementById("but-start").style.display = "none"
        document.getElementById("but-reset").style.display = "block"
    } else {
        document.getElementById("but-start").style.display = "block"
        document.getElementById("but-reset").style.display = "none"
    }
    // Data terminal
    let phase = document.getElementById("phase");
    let temperature = document.getElementById("temp");
    let engine = document.getElementById("engine");
    let rast = document.getElementById("rast");
    // steps
    let current_title = document.getElementById("currentPhase");
    let current_description = document.getElementById("currentContent");
    let next_title = document.getElementById("nextPhase");
    let next_description = document.getElementById("nextContent");

    //assign values terminal
    phase.innerHTML = data.roadmap[0][data.step];
    temperature.innerHTML = data.sensor_data.temperature;
    if (data.sensor_data.engine_mode == true) {
        engine.innerHTML = "ON";
    } else {
        engine.innerHTML = "OFF";
    }
    //assign values steps
    current_title.innerHTML = data.roadmap[0][data.step];
    current_description.innerHTML = data.roadmap[1][data.step];
    if (data.roadmap[0][data.step + 1] != undefined) {
        next_title.innerHTML = data.roadmap[0][data.step + 1];
        next_description.innerHTML = data.roadmap[1][data.step + 1];
        document.getElementById("next_step_headline").style.display = "block";
    } else {
        next_title.innerHTML = "";
        next_description.innerHTML = "";
        document.getElementById("next_step_headline").style.display = "none";
    }

    if (data.roadmap[0][data.step] == "Maischen" || data.roadmap[0][data.step] == "Würzekochen") {
        document.getElementById("rast").parentElement.style.display = "contents";
        calculateRastPhase(data);
        if (count % 3 == 0) {
            showGraph(true);
            addDatapoint(data.sensor_data.temperature);
        }
    } else {
        document.getElementById("rast").parentElement.style.display = "none";
        count = 0;
    }

    count++;
}

function next() {
    if (mode == true) {
        send_to_server("next", "")
        if (document.getElementById("chart").style.display == "block") {
            showGraph(false);
        } else if (nextPhase.innerHTML == "Würzekochen" || nextPhase.innerHTML == "Maischen" & document.getElementById("chart").style.display == "none") {
            showGraph(true);
        }
    } else {
        window.alert("Please press start first!")
    }
}

function prev() {
    if (mode == true) {
        send_to_server("prev", "")
    } else {
        window.alert("Please press start first!")
    }
}

function start() {
    if (mode == false) {
        send_to_server("start", "")
    } else {
        window.alert("Please stop the process first!")
    }
    mode = true;
}

function reset() {
    if (mode == true) {
        send_to_server("reset", "")
        location.reload();
    } else {
        window.alert("Please start the process first!")
    }
    mode = false;
}

function createGraph() {
    ctx = document.getElementById("chart").getContext("2d");

    chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: [

            ],
            datasets: [
                {
                    label: "Temperature in degrees celcius",
                    fill: false,
                    backgroundColor: "#f38301",
                    borderColor: "#f38301",
                    data: [

                    ]
                }
            ]
        },
        options: {
            title: {
                text: "Live Chart",
                display: true
            },
            maintainAspectRatio: false,
        }
    });
}

function showGraph(mode) {
    if (mode) {
        document.getElementById('chart').style.display = 'block';
    } else {
        document.getElementById('chart').style.display = 'none';
        clearChart();
    }
}

function addDatapoint(temperature) {
    // get current hours and minutes
    let date = new Date();
    chart.data.labels.push(date.getHours() + ":" + date.getMinutes());
    chart.data.datasets[0].data.push(temperature);
    chart.update();
}

function clearChart() {
    chart.data.labels = [];
    chart.data.datasets[0].data = [];
    chart.update();
}

function calculateRastPhase(data) {
    let phases = data.phases;
    console.log(phases);
    startUnix = data.start_time;
    currentUnix = Date.now() / 1000;
    delta = currentUnix - startUnix;
    console.log(currentUnix + "||" + startUnix + "||" + delta);
    console.log(delta);
    for (let i = 0; i < phases.length; i++) {
        if (delta > phases[i][1]) {
            document.getElementById("rast").innerHTML = "Phase: " + (i + 1);
        } else if (delta < phases[0][1]) {
            document.getElementById("rast").innerHTML = "Phase: 0";
        }
    }
}