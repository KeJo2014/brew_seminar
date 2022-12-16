let url = 'ws://' + window.location.host + '/ws/socket-server/';
mode = false
count = 0;
temp_cache = [];
temp_cache.eye_of_agamotto = 60;
temp_cache.currentPhase = 0;
recipeID = -1;
server_up_time = -1;
recipe = {}
done = false;
server_protocoll_response = {}
createGraph()
showGraph(false);

const chatSocket = new WebSocket(url)

chatSocket.onopen = function () {
    delay(1000).then(() => loadRecipe())
}

chatSocket.onmessage = function (e) {
    let data = JSON.parse(JSON.parse(e.data).message);
    console.log(data);
    if (data.message != null) {
        console.log("here")
        data = data.message
    }

    switch (data.command) {
        case "update":
            recipeID = data.recipe;
            server_up_time = data.brewing_up_time;
            update_site(data)
            if (data.status == "warmingUp") {
                send_to_server("keep_process", "")
                console.warn("AUFHEIZEN")
            }
            else if (data.status == "maischen" | data.status == "cooking") {
                send_to_server("keep_process", "")
            }
            break;
        case "recipe":
            recipe = {
                "name": data.name,
                "brauwasser": JSON.parse(JSON.parse(data.brauwasser)),
                "wuerzekochen": JSON.parse(JSON.parse(data.wuerzekochen)),
                "schuettung": JSON.parse(JSON.parse(data.schuettung))
            }
        case "getProcessData":
            server_protocoll_response = data.data

        default:
            console.log("that command is unknown")
            console.log(data)
            break;
    }

}

function delay(time) {
    return new Promise(resolve => setTimeout(resolve, time));
}

function send_to_server(command, msg) {
    console.log("sending:" + msg)
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
    console.log("SEND: " + JSON.stringify(text));
    chatSocket.send(JSON.stringify(text))
}

function manualEngine(mode) {
    if (mode == "on") {
        send_to_server("manual_engine", "on");
    } else if (mode == "off") {
        send_to_server("manual_engine", "off");
    } else {
        console.error("wrong mode");
    }
}

function manualTemperature(temperature) {
    send_to_server("manual_temp", temperature);
}

function update_site(data) {
    if (data.roadmap[0][data.step] == "Maischen") {
        if (count % 3 == 0) {
            showGraph(true);
            addDatapoint(data.sensor_data.temperature);
        }
    }
    if (data.roadmap[0][data.step] == "Würzekochen") {
        console.log(data.roadmap[0][data.step])
        showGraph(true);
        if (count % 3 == 0) {
            addDatapoint(data.sensor_data.temperature);
        }
    }
    // check if done
    if (data.step == data.roadmap[0].length - 1) {
        done = true;
        send_to_server("protocol_data", "-1");
        process_done();
    }
    //controll buttons
    console.log(data.status);
    if (data.step == 0) {
        if (data.status != "waiting") {
            document.getElementById("but-start").style.display = "none"
            document.getElementById("but-reset").style.display = "block"
        } else {
            document.getElementById("but-start").style.display = "block"
            document.getElementById("but-reset").style.display = "none"
        }
    } else {
        document.getElementById("but-start").style.display = "none"
        document.getElementById("but-reset").style.display = "block"
        mode = true;
    }
    // check if export icon should be displayed
    if (document.getElementById("currentPhase").innerHTML == "Gären") {
        //change icon to checklist
        loadRecipe();
    } else {
        //change icon back to right arrow
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

    if (data.roadmap[0][data.step] == "Maischen") {
        document.getElementById("rast").parentElement.style.display = "contents";
        calculateRastPhase(data, 0);
        if (count % 3 == 0) {
            showGraph(true);
            addDatapoint(data.sensor_data.temperature);
        }
    } else if (data.status == "cooking") {
        document.getElementById("rast").parentElement.style.display = "contents";
        calculateRastPhase(data, 1);
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
        if (document.getElementById("chartContainer").style.display == "block") {
            showGraph(false);
            clearChart();
            document.getElementById("important_notes").innerHTML = "";
            temp_cache.currentPhase = 0;
        } else if (nextPhase.innerHTML == "wuerzekochen" || nextPhase.innerHTML == "Maischen" & document.getElementById("chartContainer").style.display == "none") {
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
            annotation: {
                annotations: [

                ]
            }
        }
    });
}

function addChartLine() {
    console.warn("New Phase:" + chart.data.labels.length - 1)
    place = document.getElementById("rast").innerHTML
    place = place.split(" ")
    number = temp_cache.currentPhase + 1;
    place = place[0] + " " + number

    alreadyExising = false;
    chart.config.options.annotation.annotations.forEach(element => {
        if (element.label.content == place) {
            alreadyExising = true;
        }
    });
    if (alreadyExising == false) {
        chart.config.options.annotation.annotations.push({
            drawTime: "afterDatasetsDraw",
            type: "line",
            mode: "vertical",
            scaleID: "x-axis-0",
            value: chart.data.labels.length - 1,
            borderWidth: 2,
            borderColor: "gray",
            label: {
                content: place,
                enabled: true,
                position: "top"
            }
        })
    }
}

function showGraph(mode) {
    if (mode) {
        document.getElementById('chartContainer').style.display = 'block';
    } else {
        document.getElementById('chartContainer').style.display = 'none';
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
    chart.config.options.annotation.annotations = [];
    chart.update();
}

function calculateRastPhase(data, step) {
    if (data.phases != null) {
        let phases = data.phases;
        console.log(phases);
        startUnix = data.start_time;
        currentUnix = Date.now() / 1000;
        delta = currentUnix - startUnix;
        console.log(delta / temp_cache.eye_of_agamotto);
        if (step == 0) {
            for (let i = 0; i < phases.length; i++) {
                if (delta / temp_cache.eye_of_agamotto > phases[i][1]) {
                    if (i != temp_cache.currentPhase) {
                        temp_cache.currentPhase = i;
                        addChartLine();
                    }
                    document.getElementById("rast").innerHTML = "Phase: " + (i + 1);
                } else if (delta < phases[0][1]) {
                    temp_cache.currentPhase = -1;
                    document.getElementById("rast").innerHTML = "Phase: 0";
                }
            }
        } else if (step == 1) {
            for (let i = 1; i < phases.length; i++) {
                if (delta / temp_cache.eye_of_agamotto > phases[i][0][3]) {
                    if (i != temp_cache.currentPhase) {
                        temp_cache.currentPhase = i;
                        addChartLine();
                        document.getElementById("important_notes").style.color = "red"
                        document.getElementById("important_notes").innerHTML = "Jetzt Hopfen " + phases[1][i - 1][0] + " hinzugeben!";
                    }
                    document.getElementById("rast").innerHTML = "Hopfen: " + phases[1][i - 1][0];
                    document.getElementById("important_notes").style.color = "red"
                    try {
                        document.getElementById("important_notes").innerHTML = "Jetzt Hopfen " + phases[1][i - 1][0] + " hinzugeben!";
                    } catch (e) {
                        document.getElementById("important_notes").innerHTML = "";
                    }
                } else {
                    temp_cache.currentPhase = -1;
                    document.getElementById("rast").innerHTML = "zur Hopfenbeigabe bereitmachen";
                    document.getElementById("important_notes").style.color = "#f38301"
                    document.getElementById("important_notes").innerHTML = "Nächster Hopfen: " + phases[1][0][0] + " (In " + Math.round(parseInt(phases[1][0][3]) - (delta / temp_cache.eye_of_agamotto)) + " Minuten)";
                }
            }
        }
    }
}

function downloadChart() {
    date = new Date();
    day = date.toLocaleDateString();
    day = day.replace(".", "_");
    downloadName = day + "_" + document.getElementById("currentPhase").innerHTML + "_Chart.png";

    var img_b64 = chart.toBase64Image();
    var png = img_b64.split(',')[1];

    var the_file = new Blob([window.atob(png)], { type: 'image/png', encoding: 'utf-8' });

    var fr = new FileReader();
    fr.onload = function (oFREvent) {
        var v = oFREvent.target.result.split(',')[1]; // encoding is messed up here, so we fix it
        v = atob(v);
        var good_b64 = btoa(decodeURIComponent(escape(v)));
        document.getElementById("download").href = "data:image/png;base64," + good_b64;
        document.getElementById("download").download = downloadName;
        document.getElementById("download").click();
    };
    fr.readAsDataURL(the_file);
}

//create a pdf

function loadRecipe() {
    send_to_server("getRecipe", recipeID);
}

function getRecipe() {
    return recipe;
}

function getServerUpTime() {
    return server_up_time;
}

function process_done() {
    console.log("process done");
    // adjust controll buttons
    document.querySelector("#but-down").style = "display: block;";
    document.querySelector("#but-start").style = "display: none;";
    document.querySelector("#but-reset").style = "display: none;";
    document.querySelector("#but-undo").style = "display: none;";
    document.querySelector("#but-next").style = "display: none;";
}

function protocol_download() {
    console.log(server_protocoll_response)
    // get server log data
    send_to_server("protocol_data", "")
    getRecipe()
    // create protocol
    setTimeout(function () {
        console.log(server_protocoll_response)
        console.log(loadRecipe())
        let date = new Date();
        let data = [
            ["FieldID_DATUM", date.getUTCDate() + "." + (parseInt(date.getUTCMonth()) + 1) + "." + date.getFullYear()],
            ["FieldID_SUD", document.querySelector("#brewCount").innerHTML],
            ["FieldID_BIERNAME", getRecipe().name],
            ["FieldID_RAST_1", "20"],
            ["FieldID_RAST_2", "30"],
            ["FieldID_RAST_3", "10"],
            ["FieldID_ABMAISCHEN_ZEIT", "40"],
            ["FieldID_EINMAISCHEN_TEMP", "40"],
            ["FieldID_EINWEIß_TEMP", "40"],
            ["FieldID_MALTOSE_TEMP", "40"],
            ["FieldID_VERZUCKERUNG_TEMP", "40"],
            ["FieldID_ABMAISCHEN_TEMP", "40"],
            ["FieldID_KOCHEN_START_ZEIT", "12:40"],
            ["FieldID_KOCHEN_1HOPFEN", "12:50"],
            ["FieldID_KOCHEN_2HOPFEN", "13:00"],
            ["FieldID_KOCHEN_3HOPFEN", "13:20"],
            ["FieldID_KOCHEN_END_ZEIT", "13:30"],
            ["FieldID_AUSSCHLAGWUERZE_LITER", "20"],
            ["FieldID_STAMMWUERZE_PLATO", "5"],
            ["FieldID_KOCHWUERZE_LITER", "10"],
            ["FieldID_NACHGUSS_LITER", "30"]
        ]
        for (let index = 0; index < server_protocoll_response.length; index++) {
            data.push([server_protocoll_response[index].title,server_protocoll_response[server_protocoll_response[index].title]])
        }
        prepareProtocol(data);
    }, 1000);
}