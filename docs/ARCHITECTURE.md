# Architektur

```text
Home Assistant
  └─ Sicce ContrAll Custom Component
       ├─ Config Flow: Sicce-E-Mail + Passwort
       ├─ SicceClient: ThingsCloud-HTTP-Anfragen
       └─ pro Gerät ein DataUpdateCoordinator (30 Sekunden)
            ├─ Sensoren: Temperatur, Status, Firmware
            ├─ Number: Leistung, Eco-, Pause-Leistung
            ├─ Switch: Pause/Feed, Eco, Halb-Leistung
            └─ Select: Betriebsmodus
                         ↓
              Sicce ThingsCloud API
                         ↓
                 ContrAll Controller
```

Die Integration hält keine dauerhafte Bluetooth-Verbindung. Die Analyse von
ContrAll 2.33 zeigt Bluetooth für Geräteerkennung und Einrichtung, während
laufende Remote-Steuerung über Sicce ThingsCloud erfolgt. Das vermeidet
unverifizierte BLE-Schreibbefehle an sicherheitsrelevante Pumpensteuerungen.

Die API-Antworten unterscheiden sich nach Produktfamilie. Deshalb werden
Gerätefelder zur Laufzeit ausgewertet. Eine Entität wird nur erzeugt, wenn das
entsprechende Feld tatsächlich vom Gerät gemeldet wird.
