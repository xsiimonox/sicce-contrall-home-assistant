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

Die Integration legt aus Sicherheits- und Home-Assistant-Kompatibilitätsgründen
kein Dashboard automatisch an. Du aktivierst es selbst mit einer der folgenden
beiden Varianten.

### Über die Home-Assistant-Oberfläche

1. Installiere zuerst die vier Karten aus dem Abschnitt **Voraussetzungen**
   über **HACS → Frontend**. Nach jeder Installation Browser neu laden.
2. Öffne **Einstellungen → Dashboards → Dashboard hinzufügen**.
3. Wähle **Neues Dashboard erstellen**, vergib den Namen *Sicce Studio* und
   aktiviere **In Seitenleiste anzeigen**.
4. Öffne anschließend dieses Dashboard, wähle oben rechts das Drei-Punkte-Menü
   und dann **Raw configuration editor**. Kopiere den vollständigen Inhalt von
   [`dashboards/vectra_studio.yaml`](../dashboards/vectra_studio.yaml) hinein.
5. Speichern und Seite neu laden.

### Als YAML-Dashboard in `configuration.yaml`

Kopiere `dashboards/vectra_studio.yaml` nach
`/config/dashboards/vectra_studio.yaml` auf deinem Home-Assistant-System und
ergänze in `/config/configuration.yaml`:

```yaml
lovelace:
  dashboards:
    sicce-studio:
      mode: yaml
      title: Sicce Studio
      icon: mdi:water-sync
      show_in_sidebar: true
      filename: dashboards/vectra_studio.yaml
```

Starte Home Assistant anschließend vollständig neu. Das Dashboard erscheint
dann als **Sicce Studio** in der echten Home-Assistant-Seitenleiste.

Öffne danach **Entwicklerwerkzeuge → Zustände**, suche nach `sicce` und ersetze
   alle Platzhalter wie `number.sicce_pump_pump_speed` durch die Entity-ID
   deiner Pumpe.
Entferne jede Zeile, deren Entität dein Controller nicht anbietet. Das
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

Die YAML-Variante verwendet den Dashboard-Pfad `/sicce-studio`. Falls du dem
Dashboard in Home Assistant einen anderen URL-Pfad gibst, passe in den drei
Navigationskarten den Abschnitt `navigation_path` an. Die untergeordneten
Pfade bleiben `control`, `live` und `settings`.

## Logo

Das Logo im Studio-Dashboard wird standardmäßig von GitHub geladen. Wenn dein
Home-Assistant-System keinen Zugriff auf `raw.githubusercontent.com` hat,
kopiere [`logo.png`](../logo.png) nach `/config/www/sicce-studio-logo.png` und
ersetze in der Dashboard-Vorlage die Bildadresse durch:

```html
<img src="/local/sicce-studio-logo.png" width="46" height="46" alt="Sicce Studio" />
```

Die `logo.png` im Repository wird von HACS als Repository-Bild verwendet.
Damit das Logo außerdem im Kachel-Eintrag unter **Einstellungen → Geräte &
Dienste** erscheint, muss es in das offizielle Projekt
[`home-assistant/brands`](https://github.com/home-assistant/brands)
aufgenommen werden. Eine Datei innerhalb einer Custom Integration kann diese
Core-Oberfläche nicht selbst überschreiben.

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
