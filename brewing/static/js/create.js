//indices
var indexMalt = 0;
var indexWater = 0;
var indexPhase = [];
var indexHopfen = 0;
var indexPhaseDesc = 0;

var delButtonWater = document.getElementById('delButtonWater');
var delButtonMalt = document.getElementById('delButtonMalt');
var delButtonMaisch = document.getElementById('delButtonMaisch');
var delButtonHopfen = document.getElementById('delButtonHopfen');
var delButtonPhase = document.getElementById('delButtonPhase');

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
    if(indexWater > 0) {delButtonWater.style.display = 'block';}  
}

function delWater() {
    document.getElementById('guss' + indexWater).remove();
    document.getElementById('gussvol' + indexWater).remove();
    --indexWater;
    if(indexWater < 1) {delButtonWater.style.display = 'none';}
}

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
    if(indexMalt > 0) {delButtonMalt.style.display = 'block';}  
}

function delMalt() {
    document.getElementById('malz' + indexMalt).remove();
    document.getElementById('malzmenge' + indexMalt).remove();
    --indexMalt;
    if(indexMalt < 1) {delButtonMalt.style.display = 'none';}
}

function addMaischphase() {
    indexPhase.push(0);
    var inputPhaseText = document.createElement('input');
    inputPhaseText.setAttribute('type', 'text');
    inputPhaseText.setAttribute('class', 'input');
    inputPhaseText.setAttribute('id', 'maisch' + indexPhase.length);
    inputPhaseText.setAttribute('name', 'maisch' + indexPhase.length);
    inputPhaseText.setAttribute('placeholder', indexPhase.length + '. Maischphase');
    inputPhaseText.setAttribute('title', 'MAISCHPHASE');

    var inputPhaseNumber = document.createElement('input');
    inputPhaseNumber.setAttribute('type', 'number');
    inputPhaseNumber.setAttribute('class', 'input inputSpace');
    inputPhaseNumber.setAttribute('id', 'maischtemp' + indexPhase.length);
    inputPhaseNumber.setAttribute('name', 'maischtemp' + indexPhase.length);
    inputPhaseNumber.setAttribute('min', '0');
    inputPhaseNumber.setAttribute('placeholder', 'Maischtemperatur [°C]');
    inputPhaseNumber.setAttribute('title', 'MAISCHTEMPERATUR')

    var rastBox = document.createElement('div');
    rastBox.setAttribute('class', 'rastBox');
    rastBox.setAttribute('id', 'rastBox' + indexPhase.length);

    var smallerButtonsBox = document.createElement('div');
    smallerButtonsBox.setAttribute('class', 'align-items-end');
    smallerButtonsBox.setAttribute('id', 'smallerButtonsBox' + indexPhase.length);

    var buttonAddRast = document.createElement('button');
    buttonAddRast.setAttribute('type', 'button');
    buttonAddRast.setAttribute('class', 'addDelButton smallerButton');
    buttonAddRast.setAttribute('id', 'buttonAddRast' + indexPhase.length);
    buttonAddRast.setAttribute('onclick', 'addRast(' + (indexPhase.length-1)+ ')');

    var iconAddRast = document.createElement('i');
    iconAddRast.setAttribute('class', 'fa-solid fa-plus');

    var buttonDelRast = document.createElement('button');
    buttonDelRast.setAttribute('type', 'button');
    buttonDelRast.setAttribute('class', 'addDelButton smallerButton');
    buttonDelRast.setAttribute('id', 'buttonDelRast' + indexPhase.length);
    buttonDelRast.setAttribute('onclick', 'delRast('+ (indexPhase.length-1) + ')');

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
    addRast((indexPhase.length-1));
    if(indexPhase > 0) {delButtonMaisch.style.display = 'block';}  
}

function delMaischphase() {
    document.getElementById('maisch' + indexPhase.length).remove();
    document.getElementById('maischtemp' + indexPhase.length).remove();
    document.getElementById('rastBox' + indexPhase.length).remove();
    document.getElementById('smallerButtonsBox' + indexPhase.length).remove();
    indexPhase.pop();
    if(indexPhase < 1) {delButtonMaisch.style.display = 'none';}
}

function addRast(index) {
    var indexId = index + 1;
    indexPhase[index] += 1;
    var h3Rast = document.createElement('h3');
    h3Rast.setAttribute('id', 'h3Rast' + indexId + indexPhase[index]);
    var h3RastText = document.createTextNode(indexPhase[index] + '. Rast');

    var inputRastTempNumber = document.createElement('input');
    inputRastTempNumber.setAttribute('type', 'number');
    inputRastTempNumber.setAttribute('class', 'rastInput');
    inputRastTempNumber.setAttribute('id', 'rasttemp' + indexId + indexPhase[index]);
    inputRastTempNumber.setAttribute('name', 'rasttemp' + indexId + indexPhase[index]);
    inputRastTempNumber.setAttribute('min', '0');
    inputRastTempNumber.setAttribute('placeholder', 'Rasttemperatur [°C]');
    inputRastTempNumber.setAttribute('title', 'RASTTEMPERATUR');

    var inputRastDurNumber = document.createElement('input');
    inputRastDurNumber.setAttribute('type', 'number');
    inputRastDurNumber.setAttribute('class', 'rastInput inputSpace');
    inputRastDurNumber.setAttribute('id', 'rastdur' + indexId + indexPhase[index]);
    inputRastDurNumber.setAttribute('name', 'rastdur' + indexId + indexPhase[index]);
    inputRastDurNumber.setAttribute('min', '0');
    inputRastDurNumber.setAttribute('placeholder', 'Rastdauer [min]');
    inputRastDurNumber.setAttribute('title', 'RASTDAUER');

    var parent = document.querySelector('#' + 'rastBox' + indexId)
    h3Rast.appendChild(h3RastText);
    parent.appendChild(h3Rast);
    parent.appendChild(inputRastTempNumber);
    parent.appendChild(inputRastDurNumber);
    console.log(indexPhase);
}

function delRast(index) {
    var indexId = index + 1;
    document.getElementById('h3Rast' + indexId + indexPhase[index]).remove();
    document.getElementById('rasttemp' + indexId + indexPhase[index]).remove();
    document.getElementById('rastdur' + indexId + indexPhase[index]).remove();
    indexPhase[index] -= 1;
    console.log(indexPhase);
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
    if(indexHopfen > 0) {delButtonHopfen.style.display = 'block';}  
}

function delHopfen() {
    document.getElementById('hopfen' + indexHopfen).remove();
    document.getElementById('hopfenmenge' + indexHopfen).remove();
    document.getElementById('alpha' + indexHopfen).remove();
    document.getElementById('hopfentime' + indexHopfen).remove();
    --indexHopfen;
    if(indexHopfen < 1) {delButtonHopfen.style.display = 'none';}
}
function addPhase() {
    ++indexPhaseDesc;

    var inputPhaseTitleText = document.createElement('input');
    inputPhaseTitleText.setAttribute('type', 'text');
    inputPhaseTitleText.setAttribute('class', 'input');
    inputPhaseTitleText.setAttribute('id', 'phasenTitel' + indexPhaseDesc);
    inputPhaseTitleText.setAttribute('name', 'phasenTitel' + indexPhaseDesc);
    inputPhaseTitleText.setAttribute('placeholder', indexPhaseDesc + '. Titel der Phase');
    inputPhaseTitleText.setAttribute('title', 'PHASENTITEL');

    var inputPhaseDescrText = document.createElement('textarea');
    inputPhaseDescrText.setAttribute('class', 'input');
    inputPhaseDescrText.setAttribute('id', 'phasenBeschreibung' + indexPhaseDesc);
    inputPhaseDescrText.setAttribute('name', 'phasenBeschreibung' + indexPhaseDesc);
    inputPhaseDescrText.setAttribute('placeholder', 'Beschreibung der Phase...');
    inputPhaseDescrText.setAttribute('title', 'BESCHREIBUNG DER PHASE...');

    var parent = document.querySelector('#phaseBox')
    parent.appendChild(inputPhaseTitleText);
    parent.appendChild(inputPhaseDescrText);
    if(indexPhaseDesc > 0) {delButtonPhase.style.display = 'block';}  
}

function delPhase() {
    document.getElementById('phasenTitel' + indexPhaseDesc).remove();
    document.getElementById('phasenBeschreibung' + indexPhaseDesc).remove();
    --indexPhaseDesc;
    if(indexPhaseDesc < 1) {delButtonPhase.style.display = 'none';}
}

function handle_submit(){
    //brauwasser
    var brauwasser = [];
    for (let index = 1; index <= indexWater; index++) {
        var guss = document.getElementById('guss' + index).value;
        var volume = document.getElementById('gussvol' + index).value;
        brauwasser.push([guss, volume]);
    }
    var json = JSON.stringify(brauwasser);
    document.getElementById("json_brauwasser").value = json;

    //schuettung
    var schuettung = [];
    for (let index = 1; index <= indexMalt; index++) {
        var malt = document.getElementById('malz' + index).value;
        var amount = document.getElementById('malzmenge' + index).value;
        schuettung.push([malt, amount]);
    }
    var json = JSON.stringify(schuettung);
    document.getElementById("json_schuettung").value = json;
 
    //Maisch
    var maisch = [];
    for (let index = 1; index <= indexPhase.length; index++) {
        var maischI = document.getElementById('maisch' + index).value;
        var temp = document.getElementById('maischtemp' + index).value;
        var sub = [];
        for (let index2 = 1; index2 <= indexPhase[index - 1]; index2++) {
            var rasttemp = document.getElementById('rasttemp' + index + index2).value;
            var rastdur = document.getElementById('rastdur' + index + index2).value;
            sub.push([rasttemp, rastdur]);
        }
        maisch.push([maischI, temp, sub]);
    }
    var json = JSON.stringify(maisch);
    document.getElementById("json_maisch").value = json;

    //Würzekochen
    var wuerze = [];
    wuerze.push(document.getElementById('kochendur').value);
    for (let index = 1; index <= indexHopfen; index++) {
        var hop = document.getElementById('hopfen' + index).value;
        var amount = document.getElementById('hopfenmenge' + index).value;
        var acid = document.getElementById('alpha' + index).value;
        var time = document.getElementById('hopfentime' + index).value;
        wuerze.push([hop, amount, acid, time]);
    }
    var json = JSON.stringify(wuerze);
    document.getElementById("json_wuerze").value = json;

    //gaerung
    var gaerung = [];
    var sort = document.getElementById('hefe1').value;
    var temp = document.getElementById('gaertemp1').value;
    var end = document.getElementById('endgaergrad1').value;
    var carbon = document.getElementById('karbon1').value;
    gaerung.push([sort, temp, end, carbon]);
    var json = JSON.stringify(gaerung);
    document.getElementById("json_gaerung").value = json; 

    //phase
    var phase = [];
    for (let index = 1; index <= indexPhaseDesc; index++) {
        var title = document.getElementById('phasenTitel' + index).value;
        var descr = document.getElementById('phasenBeschreibung' + index).value;
        phase.push([title, descr]);
    }
    var json = JSON.stringify(phase);
    document.getElementById("json_phase").value = json; 
    //submit
    console.log(json)
    document.getElementById("form").submit();
}
