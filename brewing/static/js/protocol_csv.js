<html>

<body>

</body>
<script>
    let template = ";;;;;;;;;\n Sudbericht;;;;;;;;;\n ;;;;;;;;;\n Sud-Nr.;FieldID_SUD;;Datum:;FieldID_DATUM;;;;;\n Biersorte:;FieldID_BIERNAME;;;geplant: ;20;Liter;;;\n ;;;;;;;;;\n Schuettung gesamt:;4;kg;Pilsner Malz;90,0%;4,0;kg;;;\n ;;;Carahell;0,0%;0,0;kg;max.15%;;\n ;;;Melanoidinmalz;0,0%;0,0;kg;max.20%;;\n ;;;Frankonia Dark;0,0%;0,0;kg;max.5%;;\n ;;;Caraffa Spezial Typ 2;0,0%;0,0;kg;max.5%;;\n ;;;Caraffa Typ 1;0,0%;0,0;kg;max.5%;;\n ;;;Cara dunkel;10,0%;0,4;kg;max.30%;;\n ;;;;100,0%;;;;;\n ;;;;;;;;;\n Hauptguss:;14;Liter;;;EBC;14;14;;\n ;;;;;;;;;\n Drehzahl Pumpe umpumpen;;FieldID_PUMPEUMPUMPEN;;U/min;Vorgabe;FieldID_PUMPEUMPUMPEN_VORGABE;U/min;;\n ;;;;;;;;;\n Drehzahl Pumpe Abläutern;;FieldID_PUMPEABLÄUTERN;;U/min;Vorgabe;FieldID_PUMPEABLÄUTERN_VORGABE;U/min;;\n ;;;;;;;;;;\n Drehzahl Getriebe AHM;;FieldID_GETRIEBE;;U/min;Vorgabe;FieldID_1GETRIEBE_VORGABE;U/min;;\n ;;;;;;;;;\n Einmaischen ;61;°C;;;;;;;\n Eiweißrast;61;°C;Minuten;24;FieldID_EINWEIßRAST_ZEIT;;Uhrzeit;;\n Maltoserast;63;°C;Minuten;37;FieldID_MALTOSERAST_ZEIT;;Uhrzeit;;\n Verzuckerungsrast;72;°C;Minuten;35;FieldID_VERZUCKERUNGSRAST_ZEIT;;Uhrzeit;;\n Abmaischen;78;°C;Minuten;0;FieldID_ABMAISCHEN_ZEIT;;Uhrzeit;;\n ;;;;;;;;;\n Extrakt Vorderwuerze;FieldID_VORDERWUERZE_PLATO;°P;;lt.Programm;17,0%;°P;;;\n ;;;;;;;;;\n Nachguss;FieldID_NACHGUSS_LITER;Liter;;lt.Programm;13;Liter;;;\n ;;;;;;;;;\n Kochwuerze;FieldID_KOCHWUERZE_LITER;Liter;;lt.Programm;24;Liter;;;\n ;;;;;;;;;\n Extrakt Kochwuerze;FieldID_KOCHWUERZE_PLATO;°P;;lt.Programm;12,0;°P;;;\n ;;;;;;;;;\n ;;;;;;;;;\n Kochzeit der Wuerze:;60;Minuten;;;;;;;\n ;;;;;;;;;\n ;;;;Start:;FieldID_KOCHEN_START_ZEIT;Uhrzeit;;;\n 1. Hopfengabe:;15;g nach 0 Minuten;;;FieldID_KOCHEN_1HOPFEN;Uhrzeit;;;\n 2. Hopfengabe:;15;g nach 30 Minuten;;;FieldID_KOCHEN_2HOPFEN;Uhrzeit;;;\n 3. Hopfengabe:;11;g nach 50 Minuten;;;FieldID_KOCHEN_3HOPFEN;Uhrzeit;;;\n ;;;;Ende:;FieldID_KOCHEN_END_ZEIT;Uhrzeit;;;\n ;;;;;;;;;\n Gewuenschter Bitterstoffgehalt in  BE;;;26;;;;;;\n % Alphasäure;;;6;;;;;;\n ;;;;;;;;;\n Ausschlagwuerzemenge:;FieldID_AUSSCHLAGWUERZE_LITER;Liter;;;;;;;\n ;;;;;;;;;\n Stammwuerze: ;FieldID_STAMMWUERZE_PLATO;°P;lt.Programm;13,0%;°P;;;;\n ;;;;;;;;;\n ;;;;;;;;;\n ;;;;;;;;;\n ;;;;;;;;;\n ;;;;;;;;;\n ;Frankonia Dark;50;EBC;max.70%;;;;;\n ;Caraffa Spezial Typ 2;1150;EBC;max.5%;;;;;\n ; ;900;EBC;max.5%;;;;;\n ;Cara dunkel;110;EBC;max.30%;;;;;\n ;Pilsner Malz;3;EBC;;;;;;\n ;Carahell;25;EBC;max.15%;;;;;\n ;Melanoidinmalz;70;EBC;max.20%;;;;;\n";

    function download(filename, text) {
        var element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
        element.setAttribute('download', filename);

        element.style.display = 'none';
        document.body.appendChild(element);

        element.click();

        document.body.removeChild(element);
    }

    function prepareProtocol() {
        // get Data
        let date = new Date();
        let data = [
            ["FieldID_DATUM", date.getDay() + "." + date.getMonth() + "." + date.getFullYear()],
            ["FieldID_SUD", "Braunummer"],
            ["FieldID_BIERNAME", "Test Brauung"],
            ["FieldID_PUMPEUMPUMPEN", "30?"],
            ["FieldID_PUMPEUMPUMPEN_VORGABE", "30?"],
            ["FieldID_PUMPEABLÄUTERN_VORGABE", "30?"],
            ["FieldID_GETRIEBE", "20?"],
            ["FieldID_1GETRIEBE_VORGABE", "20?"],
            ["FieldID_EINWEIßRAST_ZEIT", "20"],
            ["FieldID_MALTOSERAST_ZEIT", "30"],
            ["FieldID_VERZUCKERUNGSRAST_ZEIT", "10"],
            ["FieldID_ABMAISCHEN_ZEIT", "40"],
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
        data.forEach(element => {
            console.log(template);
            console.log("replacing " + element[0] + " width " + element[1]);
            template = template.replaceAll(element[0], element[1]);
        });
        console.log(template);
        download("Brauprotokoll.csv", template);
    }
    prepareProtocol();
</script>

</html>
