var template = ";;;;;;;;;;;\n Sudbericht;;;;;;;;;;;\n ;;;;;;;;;;;\n Sud-Nr.;FieldID_SUD;;;;Datum:;FieldID_DATUM;;;;;\n Biersorte:;FieldID_BIERNAME;;;;;geplant: ;0;Liter;;;\n ;;;;;;;;;;;\n Schüttung gesamt:;0,00;kg;;;Pilsner Malz;90,0%;0,0;kg;;;\n ;;;;;Cara dunkel;10,0%;0,0;kg;max.30%;;\n ;;;;;;100,0%;;;;;\n ;;;;;;;;;;;\n Hauptguss:;0;Liter;;;;;;;;;\n ;;;;;;;;;;;\n ;soll:;;ist:;;;;;;;;°Plato:\n Einmaischen ;61;°C;FieldID_EINMAISCHEN_TEMP;°C;;;;;;;\n Eiweißrast;61;°C;FieldID_EINWEIß_TEMP;°C;Minuten;24;FieldID_RAST_1;;Uhrzeit;;\n Maltoserast;63;°C;FieldID_MALTOSE_TEMP;°C;Minuten;37;FieldID_RAST_2;;Uhrzeit;;\n Verzuckerungsrast;72;°C;FieldID_VERZUCKERUNG_TEMP;°C;Minuten;35;FieldID_RAST_3;;Uhrzeit;;\n Abmaischen;78;°C;FieldID_ABMAISCHEN_TEMP;°C;Minuten;0;FieldID_ABMAISCHEN_ZEIT;;Uhrzeit;;\n ;;;;;;;;;;;\n Extrakt Vorderwürze;;°P;;;;lt.Programm;17,0%;°P;;;\n ;;;;;;;;;;;\n Nachguss;;Liter;;;;lt.Programm;13;Liter;;;\n ;;;;;;;;;;;\n Kochwürze;;Liter;;;;lt.Programm;24;Liter;;;\n ;;;;;;;;;;;\n Extrakt Kochwürze;;°P;;;;lt.Programm;12,0;°P;;;\n ;;;;;;;;;;;\n ;;;;;;;;;;;\n Kochzeit der Würze:;60;Minuten;;;;;;;;;\n ;;;;;;;;;;;\n ;;;;;;Start:;FieldID_KOCHEN_START_ZEIT;Uhrzeit;;;\n 1. Hopfengabe:;15;g nach 0 Minuten;;;;;FieldID_KOCHEN_1HOPFEN;Uhrzeit;;;\n 2. Hopfengabe:;15;g nach 30 Minuten;;;;;FieldID_KOCHEN_2HOPFEN;Uhrzeit;;;\n 3. Hopfengabe:;11;g nach 50 Minuten;;;;;FieldID_KOCHEN_3HOPFEN;Uhrzeit;;;\n ;;;;;;Ende:;FieldID_KOCHEN_END_ZEIT;Uhrzeit;;;\n ;;;;;;;;;;;\n Gewünschter Bitterstoffgehalt in  BE;;;;;26;;;;;;\n % Alphasäure;;;;;6;;;;;;\n ;;;;;;;;;;;\n Ausschlagwürzemenge:;;Liter;;;;;;;;;\n ;;;;;;;;;;;\n Stammwürze: ;;°P;;;lt.Programm;13,0%;°P;;;;\n ;;;;;;;;;;;\n ;;;;;;;;;;;\n ;;;;;;;;;;;\n Gärprozess;Gärbeginn:;;;Datum:;;Temperatur:;;°C;;;\n ;Abfülldatum:;;;Datum:;;Würzegehalt:;;°P;;;\n ;;;;;;;;;;;\n ;;;;;;;;;;;\n ;;;;;;;;;;;\n ;;;;;;;;;;;\n ;;;;;;;;;;;\n ;;;;;;;;;;;\n ;;;;;;;;;;;\n";

function download(filename, text) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}

function prepareProtocol(data) {
    data.forEach(element => {
        // console.log(template);
        // console.log("replacing " + element[0] + " width " + element[1]);
        template = template.replaceAll(element[0], element[1]);
    });
    console.log(template);
    download("Brauprotokoll.csv", template);
}

