var indexMalt = 1;
var indexWater = 1;
var indexPhase = 1;
var indexRast = [1, 1];
var indexHopfen = 1;

//json
var brauwasser = [];
var schüttung = [];
var maisch = [];
var würze = [];
var gärung = [];

function addMalt() {
    ++indexMalt;
    var inputMaltText = document.createElement('input');
    inputMaltText.setAttribute('type', 'text');
    inputMaltText.setAttribute('class', 'input');
    inputMaltText.setAttribute('id', 'malz' + indexMalt);
    inputMaltText.setAttribute('name', 'malz' + indexMalt);
    inputMaltText.setAttribute('placeholder', indexMalt + '. Malzsorte');
    inputMaltText.setAttribute('title', 'MALZSORTE');

    var inputMaltNumber = document.createElement('input');
    inputMaltNumber.setAttribute('type', 'number');
    inputMaltNumber.setAttribute('class', 'input inputSpace');
    inputMaltNumber.setAttribute('id', 'malzmenge' + indexMalt);
    inputMaltNumber.setAttribute('name', 'malzmenge' + indexMalt);
    inputMaltNumber.setAttribute('min', '0');
    inputMaltNumber.setAttribute('placeholder', 'Malzmenge [g]');
    inputMaltNumber.setAttribute('title', 'MALZMENGE');

    var parent = document.querySelector('#maltBox')
    parent.appendChild(inputMaltText);
    parent.appendChild(inputMaltNumber);

}

function delMalt(id1, id2) {
    document.getElementById(id1).remove();
    document.getElementById(id2).remove();
    --indexMalt;
}

function addWater() {
    ++indexWater;
    var inputWaterText = document.createElement('input');
    inputWaterText.setAttribute('type', 'text');
    inputWaterText.setAttribute('class', 'input');
    inputWaterText.setAttribute('id', 'guss' + indexWater);
    inputWaterText.setAttribute('name', 'guss' + indexWater);
    inputWaterText.setAttribute('placeholder', indexWater + '. Guss');
    inputWaterText.setAttribute('title', 'GUSS');

    var inputWaterNumber = document.createElement('input');
    inputWaterNumber.setAttribute('type', 'number');
    inputWaterNumber.setAttribute('class', 'input inputSpace');
    inputWaterNumber.setAttribute('id', 'gussvol' + indexWater);
    inputWaterNumber.setAttribute('name', 'gussvol' + indexWater);
    inputWaterNumber.setAttribute('min', '0');
    inputWaterNumber.setAttribute('placeholder', 'Gussvolumen [l]');
    inputWaterNumber.setAttribute('title', 'GUSSVOLUMEN');

    var parent = document.querySelector('#waterBox')
    parent.appendChild(inputWaterText);
    parent.appendChild(inputWaterNumber);

}

function delWater(id1, id2) {
    document.getElementById(id1).remove();
    document.getElementById(id2).remove();
    --indexWater;
}

function addMaischphase() {
    ++indexPhase;
    indexRast.push(0);

    var inputPhaseText = document.createElement('input');
    inputPhaseText.setAttribute('type', 'text');
    inputPhaseText.setAttribute('class', 'input');
    inputPhaseText.setAttribute('id', 'maisch' + indexPhase);
    inputPhaseText.setAttribute('name', 'maisch' + indexPhase);
    inputPhaseText.setAttribute('placeholder', indexPhase + '. Maischphase');
    inputPhaseText.setAttribute('title', 'MAISCHPHASE');

    var inputPhaseNumber = document.createElement('input');
    inputPhaseNumber.setAttribute('type', 'number');
    inputPhaseNumber.setAttribute('class', 'input inputSpace');
    inputPhaseNumber.setAttribute('id', 'maischtemp' + indexPhase);
    inputPhaseNumber.setAttribute('name', 'maischtemp' + indexPhase);
    inputPhaseNumber.setAttribute('min', '0');
    inputPhaseNumber.setAttribute('placeholder', 'Maischtemperatur [°C]');
    inputPhaseNumber.setAttribute('title', 'MAISCHTEMPERATUR')

    var rastBox = document.createElement('div');
    rastBox.setAttribute('class', 'rastBox');
    rastBox.setAttribute('id', 'rastBox' + indexPhase);

    var smallerButtonsBox = document.createElement('div');
    smallerButtonsBox.setAttribute('class', 'align-items-end');
    smallerButtonsBox.setAttribute('id', 'smallerButtonsBox' + indexPhase);

    var buttonAddRast = document.createElement('button');
    buttonAddRast.setAttribute('type', 'button');
    buttonAddRast.setAttribute('class', 'addDelButton smallerButton');
    buttonAddRast.setAttribute('id', 'buttonAddRast' + indexPhase);
    buttonAddRast.setAttribute('onclick', 'addRast(' + indexPhase + ')');

    var iconAddRast = document.createElement('i');
    iconAddRast.setAttribute('class', 'fa-solid fa-plus');

    var buttonDelRast = document.createElement('button');
    buttonDelRast.setAttribute('type', 'button');
    buttonDelRast.setAttribute('class', 'addDelButton smallerButton');
    buttonDelRast.setAttribute('id', 'buttonDelRast' + indexPhase);
    buttonDelRast.setAttribute('onclick', 'delRast('+ indexPhase + ')');

    var iconDelRast = document.createElement('i');
    iconDelRast.setAttribute('class', 'fa-solid fa-minus');

    var parent = document.querySelector('#maischBox')
    buttonAddRast.appendChild(iconAddRast);
    buttonDelRast.appendChild(iconDelRast);
    smallerButtonsBox.appendChild(buttonAddRast);
    smallerButtonsBox.appendChild(buttonDelRast);
    parent.appendChild(inputPhaseText);
    parent.appendChild(inputPhaseNumber);
    parent.appendChild(rastBox);
    parent.appendChild(smallerButtonsBox);

}

function delMaischphase() {
    document.getElementById('maisch' + indexPhase).remove();
    document.getElementById('maischtemp' + indexPhase).remove();
    document.getElementById('rastBox' + indexPhase).remove();
    document.getElementById('smallerButtonsBox' + indexPhase).remove();
    indexRast[indexPhase] = 0;
    --indexPhase;
}

function addRast(index) {
    indexRast[index] += 1;

    var h3Rast = document.createElement('h3');
    h3Rast.setAttribute('id', 'h3Rast' + indexPhase + indexRast[index]);
    var h3RastText = document.createTextNode(indexRast[index] + '. Rast');

    var inputRastTempNumber = document.createElement('input');
    inputRastTempNumber.setAttribute('type', 'number');
    inputRastTempNumber.setAttribute('class', 'rastInput');
    inputRastTempNumber.setAttribute('id', 'rasttemp' + indexPhase + indexRast[index]);
    inputRastTempNumber.setAttribute('name', 'rasttemp' + indexPhase + indexRast[index]);
    inputRastTempNumber.setAttribute('min', '0');
    inputRastTempNumber.setAttribute('placeholder', 'Rasttemperatur [°C]');
    inputRastTempNumber.setAttribute('title', 'RASTTEMPERATUR');

    var inputRastDurNumber = document.createElement('input');
    inputRastDurNumber.setAttribute('type', 'number');
    inputRastDurNumber.setAttribute('class', 'rastInput inputSpace');
    inputRastDurNumber.setAttribute('id', 'rastdur' + indexPhase + indexRast[index]);
    inputRastDurNumber.setAttribute('name', 'rastdur' + indexPhase + indexRast[index]);
    inputRastDurNumber.setAttribute('min', '0');
    inputRastDurNumber.setAttribute('placeholder', 'Rastdauer [min]');
    inputRastDurNumber.setAttribute('title', 'RASTDAUER');

    var parent = document.querySelector('#' + 'rastBox' + index)
    h3Rast.appendChild(h3RastText);
    parent.appendChild(h3Rast);
    parent.appendChild(inputRastTempNumber);
    parent.appendChild(inputRastDurNumber);

}

function delRast(index) {
    document.getElementById('h3Rast' + index + indexRast[index]).remove();
    document.getElementById('rasttemp' + index + indexRast[index]).remove();
    document.getElementById('rastdur' + index + indexRast[index]).remove();
    indexRast[index] -= 1;

}

function addHopfen() {
    ++indexHopfen;

    var inputHopfenText = document.createElement('input');
    inputHopfenText.setAttribute('type', 'text');
    inputHopfenText.setAttribute('class', 'input');
    inputHopfenText.setAttribute('id', 'hopfen' + indexHopfen);
    inputHopfenText.setAttribute('name', 'hopfen' + indexHopfen);
    inputHopfenText.setAttribute('placeholder', indexHopfen + '. Hopfensorte');
    inputHopfenText.setAttribute('title', 'HOPFENSORTE');

    var inputHopfenMengeNumber = document.createElement('input');
    inputHopfenMengeNumber.setAttribute('type', 'number');
    inputHopfenMengeNumber.setAttribute('class', 'input');
    inputHopfenMengeNumber.setAttribute('id', 'hopfenmenge' + indexHopfen);
    inputHopfenMengeNumber.setAttribute('name', 'hopfenmenge' + indexHopfen);
    inputHopfenMengeNumber.setAttribute('min', '0');
    inputHopfenMengeNumber.setAttribute('placeholder', 'Hopfenmenge [g]');
    inputHopfenMengeNumber.setAttribute('title', 'HOPFENMENGE');

    var inputHopfenAlphaNumber = document.createElement('input');
    inputHopfenAlphaNumber.setAttribute('type', 'number');
    inputHopfenAlphaNumber.setAttribute('class', 'input');
    inputHopfenAlphaNumber.setAttribute('id', 'alpha' + indexHopfen);
    inputHopfenAlphaNumber.setAttribute('name', 'alpha' + indexHopfen);
    inputHopfenAlphaNumber.setAttribute('min', '0');
    inputHopfenAlphaNumber.setAttribute('placeholder', 'α-Säure [%]');
    inputHopfenAlphaNumber.setAttribute('title', 'ALPHASÄURE');

    var inputHopfenTimeNumber = document.createElement('input');
    inputHopfenTimeNumber.setAttribute('type', 'text');
    inputHopfenTimeNumber.setAttribute('class', 'input inputSpace');
    inputHopfenTimeNumber.setAttribute('id', 'hopfentime' + indexHopfen);
    inputHopfenTimeNumber.setAttribute('name', 'hopfentime' + indexHopfen);
    inputHopfenTimeNumber.setAttribute('placeholder', 'Hopfenzugabe vor Kochende [min]');
    inputHopfenTimeNumber.setAttribute('title', 'HOPFENZUGABE');

    var parent = document.querySelector('#hopfenBox')
    parent.appendChild(inputHopfenText);
    parent.appendChild(inputHopfenMengeNumber);
    parent.appendChild(inputHopfenAlphaNumber);
    parent.appendChild(inputHopfenTimeNumber );

}

function delHopfen(id1, id2, id3, id4) {
    document.getElementById(id1).remove();
    document.getElementById(id2).remove();
    document.getElementById(id3).remove();
    document.getElementById(id4).remove();
    --indexHopfen;
}

function handle_submit(){
    //brauwasser
    for (let index = 1; index <= indexWater; index++) {
        var guss = document.getElementById('guss' + index).value;
        var volume = document.getElementById('gussvol' + index).value;
        var entry = [guss, volume];
        brauwasser.push(entry);
    }
    var json = JSON.stringify(brauwasser);
    document.getElementById("json_brauwasser").value = json;
    //schüttung
    for (let index = 1; index <= indexMalt; index++) {
        var malt = document.getElementById('malz' + index).value;
        var amount = document.getElementById('malzmenge' + index).value;
        var entry = [malt, amount];
        schüttung.push(entry);
    }
    var json = JSON.stringify(schüttung);
    document.getElementById("json_schuettung").value = json;
    //Maisch
    for (let index = 1; index <= indexPhase; index++) {
        var maischi = document.getElementById('maisch' + index).value;
        var temp = document.getElementById('maischtemp' + index).value;
        var sub = [];
        for (let index2 = 1; index2 <= indexRast[1]; index2++) {
            var rasttemp = document.getElementById('rasttemp' + index + index2).value;
            var rastdur = document.getElementById('rastdur' + index + index2).value;
            var micro_entry = [rasttemp, rastdur];
            sub.push(micro_entry);
        }
        var entry = [maischi, temp, sub];
        maisch.push(entry);
    }
    var json = JSON.stringify(maisch);
    document.getElementById("json_maisch").value = json;
    //Würzekochen
    würze.push(document.getElementById('kochendur').value);
    for (let index = 1; index <= indexHopfen; index++) {
        var hop = document.getElementById('hopfen' + index).value;
        var amount = document.getElementById('hopfenmenge' + index).value;
        var acid = document.getElementById('alpha' + index).value;
        var time = document.getElementById('hopfentime' + index).value;
        var entry = [hop, amount, acid, time];
        würze.push(entry);
    }
    var json = JSON.stringify(würze);
    document.getElementById("json_wuerze").value = json;
    //gärung
    var sort = document.getElementById('hefe1').value;
    var temp = document.getElementById('gaertemp1').value;
    var end = document.getElementById('endgaergrad1').value;
    var carbon = document.getElementById('karbon1').value;
    var entry = [sort, temp, end, carbon];
    gärung.push(entry);
    var json = JSON.stringify(gärung);
    document.getElementById("json_gaerung").value = json;

    //submit
    document.getElementById("form").submit();
}
