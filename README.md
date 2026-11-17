# Sicce ContrAll for Home Assistant

This custom component brings Sicce ContrAll cloud-connected devices into Home
Assistant. It signs in using the same email address and password as ContrAll
and uses production API locations found in ContrAll 2.33
(`sicce.thingscloud.it/api`, `/mobile/login`, `/v2/settings`,
`/v2/pauseDevice`) rather than an unverified BLE protocol.

> [!WARNING]
> Diese frühe Version verwendet die Sicce-Cloud-API. Die Steuerung einer Pumpe
> kann Wasserbewegung sofort verändern. Teste neue Automationen zunächst bei
> Anwesenheit und verwende keine kritischen Sicherheitsfunktionen als alleinige
> Home-Assistant-Automation.

## Funktionen

- Entdeckung aller zum ContrAll-Konto gehörenden Cloud-Geräte
- Pumpenleistung, Eco- und Pause-Leistung, wenn vom Controller gemeldet
- Pause-/Feed-Modus über den aus der App belegten ContrAll-v2-Befehl
- Modus-, Energie- und Halb-Leistungs-Steuerung, sofern unterstützt
- Temperatur-, Status- und Firmware-Entitäten
- Robustes dynamisches Feld-Mapping für verschiedene Sicce-Produktfamilien

## Installation

Copy `custom_components/sicce_contrall` to Home Assistant's
`config/custom_components/` directory and restart Home Assistant. Then add
**Sicce ContrAll** in *Settings → Devices & services*.

Use the email address and password of your ContrAll account. The integration
logs in via the mobile API when Home Assistant starts; credentials are never
written to logs. Treat Home Assistant configuration backups as sensitive,
because config-entry credentials are included. The default API URL is already
set.

Ausführliche Hinweise: [Einrichtung](docs/SETUP.md),
[Architektur](docs/ARCHITECTURE.md) und
[Protokollstand](docs/PROTOCOL_RESEARCH.md).

## Entitäten

The component discovers fields returned by each controller, so it works across
the supported pump, heater and controller families without inventing controls
for a device that does not offer them:

- pump speed, Eco speed and pause speed numbers (when supplied by the cloud)
- pause/feed-mode switch (`/v2/pauseDevice`)
- Eco/half-power switches and mode selector where the device reports them
- temperature, status and firmware sensors
- per-device refresh button

Devices are polled every 30 seconds. A command is followed by a refresh;
Home Assistant only presents controls whose matching field was returned by
the controller.

## Protokollgrenze

The APK shows that Bluetooth is used for setup/discovery, while the ongoing
controller interface uses ThingsCloud. This component deliberately does not
attempt to send guessed BLE writes to a water pump. Capturing one authenticated
ContrAll session for a specific model would allow remaining controller request
bodies and responses to be verified.

## Entwicklung

```sh
python -m compileall custom_components/sicce_contrall
git diff --check
```

Siehe auch [CONTRIBUTING.md](CONTRIBUTING.md).
