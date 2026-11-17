# Einrichtung

## Voraussetzungen

- Home Assistant 2024.8 oder neuer
- Ein Sicce-Gerät, das in der ContrAll-App unter demselben ThingsCloud-Konto
  sichtbar und online ist
- Die E-Mail-Adresse und das Passwort deines ContrAll-Kontos

## Installation über HACS

1. Öffne in HACS **Custom repositories**.
2. Füge die URL dieses Repositorys als Typ **Integration** hinzu.
3. Suche nach **Sicce ContrAll**, installiere die Integration und starte Home
   Assistant neu.
4. Öffne **Einstellungen → Geräte & Dienste → Integration hinzufügen** und
   wähle **Sicce ContrAll**.
5. Trage E-Mail-Adresse und Passwort deines ContrAll-Kontos ein. Die Standard-API-URL muss normalerweise nicht
   geändert werden.

## Manuelle Installation

Kopiere den Ordner `custom_components/sicce_contrall` nach
`/config/custom_components/` deiner Home-Assistant-Installation und starte
Home Assistant neu.

## Zugangsdaten-Hinweise

Die Integration nutzt den in ContrAll 2.33 nachgewiesenen mobilen Login unter
`/mobile/login`. Das Passwort wird nicht protokolliert. Behandle
Home-Assistant-Backups dennoch wie vertrauliche Daten, da Config-Entries
Zugangsdaten enthalten.

## Fehlersuche

- **Keine Geräte gefunden:** Prüfe, ob die Pumpe in ContrAll online ist und
  der Token zum gleichen Konto gehört.
- **Anmeldung fehlgeschlagen:** Prüfe E-Mail-Adresse und Passwort zunächst in
  der ContrAll-App.
- **Entität fehlt:** Die Integration zeigt Steuerungen nur an, wenn der
  jeweilige Controller das zugehörige Feld in seiner Antwort liefert.
- **Gerät nicht verfügbar:** Prüfe die Internetverbindung des Controllers und
  anschließend die ContrAll-App.

Aktiviere bei Bedarf das Debug-Logging:

```yaml
logger:
  logs:
    custom_components.sicce_contrall: debug
```
