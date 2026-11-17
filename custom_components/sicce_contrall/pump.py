"""Speed controls used by the ContrAll 2.33 pump screens."""
from math import isfinite

LEGACY_MODELS = (2, 3, 4, 5, 15)
PSK_MODELS = (8, 10, 11, 12)
LEGACY_SPEEDS = (5, 10, 14, 19, 24, 29, 33, 38, 43, 48, 52, 57, 62, 67, 71, 76, 81, 86, 90, 95, 100)


def speed_field(device):
    """Return the field used by the app's upper speed control."""
    model = device.get("device_model_id")
    if type(model) is not int:
        return None
    if model in LEGACY_MODELS:
        return "power"
    if model in PSK_MODELS:
        return "program_v1"
    if model in (6, 9, 14) and not device.get("is_whale"):
        preset = device.get("preset")
        if type(preset) is int:
            single_cursor_preset = 2 if model == 9 else 3
            return "program_v1" if preset == single_cursor_preset else "program_v2"
    return None


def speed_percent(device):
    """Return the configured percentage only when the app's field is present."""
    value = device.get(speed_field(device))
    if type(value) in (float, int) and 0 <= value <= 100:
        return value
    return None


def speed_command(device, requested):
    """Build the same model-specific speed request as ContrAll."""
    field = speed_field(device)
    if field is None or speed_percent(device) is None:
        raise ValueError("ContrAll did not provide a supported pump speed")
    if not isfinite(requested) or not 5 <= requested <= 100 or int(requested) != requested:
        raise ValueError("Pump speed must be a whole percentage between 5 and 100")
    speed = int(requested)
    model = device["device_model_id"]
    if model in LEGACY_MODELS:
        speed = min(LEGACY_SPEEDS, key=lambda allowed: abs(allowed - speed))
        return "/status", {**device, "power": speed, "updating": True}, speed

    fields = {"program_preset": "program_preset", "program": "preset", "mode": "mode",
              "v1": "program_v1", "v2": "program_v2", "t1": "program_t1", "t2": "program_t2"}
    if any(type(device.get(key)) not in (int, float) for key in fields.values()):
        raise ValueError("ContrAll did not provide the full active pump program")
    if field == "program_v2" and speed < device["program_v1"] + 5:
        raise ValueError("Maximum speed must be at least five points above the program's minimum speed")
    payload = {target: device[source] for target, source in fields.items()}
    if model == 9:
        payload["t1"] /= 10
        payload["t2"] /= 10
    payload["v1" if field == "program_v1" else "v2"] = speed
    payload["start"] = 0
    return "/v2/program", payload, speed
