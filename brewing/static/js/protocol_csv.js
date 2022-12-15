var template = ";;;;;;;;;;; Sudbericht;;;;;;;;;;; ;;;;;;;;;;; Sud-Nr.;FieldID_SUD;;;;Datum:;FieldID_DATUM;;;;; Biersorte:;FieldID_BIERNAME;;;;;geplant: ;0;Liter;;; ;;;;;;;;;;; Schüttung gesamt:;0,00;kg;;;Pilsner Malz;90,0%;0,0;kg;;; ;;;;;Cara dunkel;10,0%;0,0;kg;max.30%;; ;;;;;;100,0%;;;;; ;;;;;;;;;;; Hauptguss:;0;Liter;;;;;;;;; ;;;;;;;;;;; ;soll:;;ist:;;;;;;;;°Plato: Einmaischen ;61;°C;FieldID_EINMAISCHEN_TEMP;°C;;;;;;; Eiweißrast;61;°C;FieldID_EINWEIß_TEMP;°C;Minuten;24;FieldID_EINWEIßRAST_ZEIT;;Uhrzeit;; Maltoserast;63;°C;FieldID_MALTOSE_TEMP;°C;Minuten;37;FieldID_MALTOSERAST_ZEIT;;Uhrzeit;; Verzuckerungsrast;72;°C;FieldID_VERZUCKERUNG_TEMP;°C;Minuten;35;FieldID_VERZUCKERUNGSRAST_ZEIT;;Uhrzeit;; Abmaischen;78;°C;FieldID_ABMAISCHEN_TEMP;°C;Minuten;0;FieldID_ABMAISCHEN_ZEIT;;Uhrzeit;; ;;;;;;;;;;; Extrakt Vorderwürze;;°P;;;;lt.Programm;17,0%;°P;;; ;;;;;;;;;;; Nachguss;;Liter;;;;lt.Programm;13;Liter;;; ;;;;;;;;;;; Kochwürze;;Liter;;;;lt.Programm;24;Liter;;; ;;;;;;;;;;; Extrakt Kochwürze;;°P;;;;lt.Programm;12,0;°P;;; ;;;;;;;;;;; ;;;;;;;;;;; Kochzeit der Würze:;60;Minuten;;;;;;;;; ;;;;;;;;;;; ;;;;;;Start:;FieldID_KOCHEN_START_ZEIT;Uhrzeit;;; 1. Hopfengabe:;15;g nach 0 Minuten;;;;;FieldID_KOCHEN_1HOPFEN;Uhrzeit;;; 2. Hopfengabe:;15;g nach 30 Minuten;;;;;FieldID_KOCHEN_2HOPFEN;Uhrzeit;;; 3. Hopfengabe:;11;g nach 50 Minuten;;;;;FieldID_KOCHEN_3HOPFEN;Uhrzeit;;; ;;;;;;Ende:;FieldID_KOCHEN_END_ZEIT;Uhrzeit;;; ;;;;;;;;;;; Gewünschter Bitterstoffgehalt in  BE;;;;;26;;;;;; % Alphasäure;;;;;6;;;;;; ;;;;;;;;;;; Ausschlagwürzemenge:;;Liter;;;;;;;;; ;;;;;;;;;;; Stammwürze: ;;°P;;;lt.Programm;13,0%;°P;;;; ;;;;;;;;;;; ;;;;;;;;;;; ;;;;;;;;;;; Gärprozess;Gärbeginn:;;;Datum:;;Temperatur:;;°C;;; ;Abfülldatum:;;;Datum:;;Würzegehalt:;;°P;;; ;;;;;;;;;;; ;;;;;;;;;;; ;;;;;;;;;;; ;;;;;;;;;;; ;;;;;;;;;;; ;;;;;;;;;;; ;;;;;;;;;;;";

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

