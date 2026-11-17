# Protokollstand

Diese Integration wurde gegen `SICCE ContrAll 2.33` analysiert. Folgende
Punkte sind aus dem App-Bundle direkt belegt:

| Bereich | Befund |
| --- | --- |
| Produktions-API | `https://sicce.thingscloud.it/api` |
| Einstellungen | `/v2/settings` |
| Pause | `/v2/pauseDevice` |
| Cloud-Funktion | Geräte, Firmware, Zeitpläne, WLAN-Status und Remote-Steuerung |
| Bluetooth | Scan und Einrichtung, insbesondere WLAN-Provisionierung |

Nicht als stabiler öffentlicher Vertrag behandelt werden Login-Endpunkte,
Token-Erneuerung, gerätespezifische Request-Bodies und BLE-Charakteristiken.
Sie werden erst nach reproduzierbaren Aufzeichnungen ergänzt. Das schützt
insbesondere vor falschen Geschwindigkeits- oder Pausenbefehlen.

## Beiträge zur Protokollunterstützung

Bitte niemals Tokens, Passwörter, MAC-Adressen oder Seriennummern veröffentlichen.
Hilfreich sind anonymisierte HTTP-Methode, Pfad, Request-/Response-Schema,
Modellname und Firmware-Version. Vor einem neuen Schreibbefehl muss mindestens
ein erfolgreicher Readback auf einem echten Gerät dokumentiert sein.
