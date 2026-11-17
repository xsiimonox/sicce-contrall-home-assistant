# Protokollstand

Diese Integration wurde gegen `SICCE ContrAll 2.33` analysiert. Folgende
Punkte sind aus dem App-Bundle direkt belegt:

| Bereich | Befund |
| --- | --- |
| Produktions-API | `https://sicce.thingscloud.it/api` |
| Konto-Anmeldung | `POST /mobile/login` mit `email` und `password` |
| Pumpendetails | `GET /devices/{id}`, Gerätedaten unter `data` |
| Leistung (ältere SDC-Modelle) | `POST /devices/{id}/status` mit `power` im Gerätezustand |
| Leistung (neuere Modelle) | `POST /devices/{id}/v2/program` mit dem aktiven Programm und geändertem `v1` oder `v2` |
| Pause | `/v2/pauseDevice` |
| Cloud-Funktion | Geräte, Firmware, Zeitpläne, WLAN-Status und Remote-Steuerung |
| Bluetooth | Scan und Einrichtung, insbesondere WLAN-Provisionierung |

Nicht als stabiler öffentlicher Vertrag behandelt werden Token-Erneuerung,
gerätespezifische Request-Bodies und BLE-Charakteristiken.

Das Feld `power` kann bei programmierbaren Pumpen 0 sein, obwohl das aktive
Programm einen höheren Sollwert hat. Der Regler verwendet dieselben
Programmfelder wie die App. Nach dem Schreiben liest die Integration den
Sollwert zurück. Diese Prüfung bestätigt die Einstellung in der Cloud.
Sie werden erst nach reproduzierbaren Aufzeichnungen ergänzt. Das schützt
insbesondere vor falschen Geschwindigkeits- oder Pausenbefehlen.

## Beiträge zur Protokollunterstützung

Bitte niemals Tokens, Passwörter, MAC-Adressen oder Seriennummern veröffentlichen.
Hilfreich sind anonymisierte HTTP-Methode, Pfad, Request-/Response-Schema,
Modellname und Firmware-Version. Vor einem neuen Schreibbefehl muss mindestens
ein erfolgreicher Readback auf einem echten Gerät dokumentiert sein.
