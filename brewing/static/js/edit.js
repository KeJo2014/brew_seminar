var indexMalt = 0;
var indexWater = 0;
var indexPhase = 0;
var indexRast = [0,0];
var indexHopfen = 0;
var indexPhaseDesc = 0;


var brauwasserElement = document.getElementById('brauwasser');
var brauwasserJson = brauwasserElement.getAttribute('value'); 
var brauwasserArray = JSON.parse(brauwasserJson);

for (let i = 0; i < brauwasserArray.length; i++)
{
    addWater(brauwasserArray[i][0], brauwasserArray[i][1]); 
}

//var phaseElement = document.getElementById('phase');
//var phaseJson = phaseElement.getAttribute('value'); 
//var phaseArray = JSON.parse(phaseJson); 

//for (let i = 0; i < phaseArray.length; i++)
// {
//     addPhase(phaseArray[i][0], phaseArray[i][1]); 
// }

var schuettungElement = document.getElementById('schuettung');
var schuettungJson = schuettungElement.getAttribute('value'); 
console.log(schuettungJson);
var schuettungArray = JSON.parse(schuettungJson);

for (let i = 0; i < schuettungArray.length; i++)
{
    addMalt(schuettungArray[i][0], schuettungArray[i][1]); 
}

// var maischplanElement = document.getElementById('maischplan');
// var maischplanJson = maischplanElement.getAttribute('value'); 
// var maischplanArray = JSON.parse(maischplanJson);
// var rastArray;

// for (let i = 0; i < maischplanArray.length; i++)
// {
//     addMaischphase(maischplanArray[i][0], maischplanArray[i][1]); 
//     rastArray = maischplanArray[i][2];
//     for (let j = 0; j < rastArray.length; j++)
//     {
//         addRast(indexPhase, rastArray[j][0], rastArray[j][1]); 
//     }
// }

// var kochenElement = document.getElementById('kochen');
// var kochenJson = kochenElement.getAttribute('value'); 
// var kochenArray = JSON.parse(kochenJson);

// var kochenDurElement = document.getElementById('kochendur');
// kochenDurElement.setAttribute('value', kochenArray[0]);

// for (let i = 1; i < kochenArray.length; i++)
// {
//     addHopfen(kochenArray[i][0], kochenArray[i][1], kochenArray[i][2], kochenArray[i][3]); 
// }

// var gaerungElement = document.getElementById('gaerung');
// var gaerungJson = gaerungElement.getAttribute('value'); 
// var gaerungArray = JSON.parse(gaerungJson);

// var gaerungHefeElement = document.getElementById('hefe1');
// gaerungHefeElement.setAttribute('value', gaerungArray[0][0]);

// var gaerungTempElement = document.getElementById('gaertemp1');
// gaerungTempElement.setAttribute('value', gaerungArray[0][1]);

// var gaerungGradElement = document.getElementById('endgaergrad1');
// gaerungGradElement.setAttribute('value', gaerungArray[0][2]);

// var gaerungKarbonElement = document.getElementById('karbon1');
// gaerungKarbonElement.setAttribute('value', gaerungArray[0][3]);


function handle_update(){
    document.getElementById("edit_form").submit();
}
