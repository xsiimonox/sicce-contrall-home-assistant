# Sicce Studio in der Home-Assistant-Seitenleiste

Ab Version 0.3.0 registriert die Integration selbst einen Eintrag
**Sicce Studio** in der echten Home-Assistant-Seitenleiste. Das ist kein
Lovelace-Dashboard und muss nicht manuell importiert werden.

## Aktivierung

1. Aktualisiere die Integration in HACS auf Version 0.3.0 oder neuer.
2. Starte Home Assistant vollständig neu, nicht nur die Integration.
3. Lade die Home-Assistant-Oberfläche hart neu. Im Browser hilft
   `Strg`/`Cmd` + `Shift` + `R`; in der Companion App die Ansicht schließen
   und erneut öffnen.
4. Der Eintrag **Sicce Studio** mit dem Wasserwirbel-Logo erscheint links in
   der Seitenleiste.

Der Eintrag wird erst registriert, nachdem mindestens ein Sicce-ContrAll-
Config-Entry erfolgreich geladen wurde. Wenn er fehlt, öffne zuerst
**Einstellungen → Geräte & Dienste → Sicce ContrAll** und prüfe, ob die
Integration eingerichtet und kein Einrichtungsfehler angezeigt wird.

Der Studio-Eintrag ist standardmäßig nur für Home-Assistant-Administratoren
sichtbar. Das schützt die direkte Pumpensteuerung vor nicht-administrativen
Benutzern.

## Was die Studio-Seite steuert

- von der Integration gemeldete Pumpenleistung
- Pause/Stopp und Weiter über den Sicce-Pause-Modus
- Aktualisierung der Controller-Daten
- Status, Temperatur und Firmware, sofern der Controller diese Werte liefert

Der Stopp ist eine Sicce-Pause und keine Netztrennung. Für eine zeitgesteuerte
Pause bleibt die beigefügte
[`sicce_pause_timer.yaml`](../examples/sicce_pause_timer.yaml) die robuste
Home-Assistant-Lösung.
