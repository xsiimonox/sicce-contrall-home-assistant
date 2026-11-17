# Sicce Studio Dashboard

`dashboards/vectra_studio.yaml` ist eine dunkle, Vectra-Studio-inspirierte
Dashboard-Vorlage für einen Sicce-Controller. Sie liefert eine feste
Seitenleiste, eine große Flow-Anzeige, Schnellaktionen und separate Ansichten
für Steuerung und Telemetrie.

Das Sicce-Studio-Logo wird automatisch im Kopf der Seitenleiste geladen. Es
liegt außerdem als `logo.png` und `icon.png` im Repository vor und wird damit
auch in HACS als Repository-Bild verwendet.

## Voraussetzungen

Installiere in HACS unter **Frontend** diese Karten und lade danach den Browser
neu:

- `button-card`
- `Mushroom`
- `layout-card`
- `card-mod`

## Einrichten

1. Öffne **Einstellungen → Dashboards → Dashboard hinzufügen** und wähle
   **Neues Dashboard von Grund auf** mit dem Typ *YAML*.
2. Kopiere den Inhalt von
   [`dashboards/vectra_studio.yaml`](../dashboards/vectra_studio.yaml) in die
   YAML-Konfiguration.
3. Öffne **Entwicklerwerkzeuge → Zustände**, suche nach `sicce` und ersetze
   alle Platzhalter wie `number.sicce_pump_pump_speed` durch die Entity-ID
   deiner Pumpe.
4. Entferne jede Zeile, deren Entität dein Controller nicht anbietet. Das
   betrifft je nach Modell zum Beispiel Eco, Pause-Geschwindigkeit, Modus,
   Temperatur oder Firmware.

## Aus, Pause und Pausen-Timer

Kopiere zusätzlich [`examples/sicce_pause_timer.yaml`](../examples/sicce_pause_timer.yaml)
als Home-Assistant-Paket oder übernimm dessen Abschnitte `timer`, `script` und
`automation` in die jeweiligen Konfigurationsdateien. Ersetze darin
`switch.sicce_pump_pause` durch deine tatsächliche Pause-Entität.

Danach stehen in Studio drei eindeutige Aktionen bereit:

- **AUS / Stopp** aktiviert die von Sicce bestätigte Pause sofort und bleibt
  aktiv, bis du **Weiter** drückst.
- **Pause 15 min** pausiert die Pumpe und startet den Timer. Nach 15 Minuten
  schaltet die Automation die Pumpe selbständig wieder ein.
- **Weiter** bricht einen Timer ab und beendet die Pause sofort.

„AUS / Stopp“ ist bewusst kein elektrischer Netzschalter. Die Integration
verwendet dafür ausschließlich den Sicce-Pause-Befehl. Verwende ihn nicht als
Sicherheitsabschaltung; für Wartung ist eine sichere Trennung vom Stromkreis
erforderlich.

Das Beispiel nennt die Views über `/dashboard-sicce/...`. Falls dein Dashboard
einen anderen URL-Pfad hat, passe in den vier Navigationskarten den Abschnitt
`navigation_path` an. Die untergeordneten Pfade bleiben `control`, `live` und
`settings`.

## Entity-Beispiel

Die tatsächlichen Namen hängen vom Gerätenamen in Home Assistant ab. Ein
typisches Mapping sieht so aus:

| Bereich | Beispiel-Entität |
| --- | --- |
| Durchfluss | `number.meine_sicce_pumpe_pump_speed` |
| Futterpause | `switch.meine_sicce_pumpe_pause` |
| Eco | `switch.meine_sicce_pumpe_eco_mode` |
| Temperatur | `sensor.meine_sicce_pumpe_water_temperature` |
| Aktualisieren | `button.meine_sicce_pumpe_refresh` |

Die Geschwindigkeitskarte verwendet die echte `number`-Entität. Sie zeigt
damit immer den von der Integration zurückgemeldeten Sollwert an und löst beim
Antippen den normalen Home-Assistant-Regler aus.
