# Einrichtung

## Voraussetzungen

- Home Assistant 2024.8 oder neuer
- Ein Sicce-Gerät, das in der ContrAll-App unter demselben ThingsCloud-Konto
  sichtbar und online ist
- Ein ThingsCloud-Bearer-Token

## Installation über HACS

1. Öffne in HACS **Custom repositories**.
2. Füge die URL dieses Repositorys als Typ **Integration** hinzu.
3. Suche nach **Sicce ContrAll**, installiere die Integration und starte Home
   Assistant neu.
4. Öffne **Einstellungen → Geräte & Dienste → Integration hinzufügen** und
   wähle **Sicce ContrAll**.
5. Trage den Bearer-Token ein. Die Standard-API-URL muss normalerweise nicht
   geändert werden.

## Manuelle Installation

Kopiere den Ordner `custom_components/sicce_contrall` nach
`/config/custom_components/` deiner Home-Assistant-Installation und starte
Home Assistant neu.

## Token-Hinweise

ContrAll stellt derzeit keine dokumentierte, stabile OAuth- oder Passwort-API
bereit. Deshalb fragt die Integration bewusst nach einem bereits vorhandenen
Bearer-Token, anstatt Zugangsdaten zu speichern oder Login-Anfragen zu raten.

Ein Token berechtigt wie eine angemeldete ContrAll-Sitzung. Behandle ihn wie
ein Passwort, teile ihn nicht in Issues und sichere Home-Assistant-Backups
angemessen. Wenn Sicce den Token widerruft oder er abläuft, lege den Eintrag
neu an.

## Fehlersuche

- **Keine Geräte gefunden:** Prüfe, ob die Pumpe in ContrAll online ist und
  der Token zum gleichen Konto gehört.
- **401/403:** Token ist ungültig, abgelaufen oder besitzt keine Berechtigung.
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
