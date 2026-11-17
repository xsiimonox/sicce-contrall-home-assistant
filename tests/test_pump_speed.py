"""Regression cases for the speed state and commands used by ContrAll."""
import unittest

from custom_components.sicce_contrall.pump import speed_command, speed_percent


class TestPumpSpeed(unittest.TestCase):
    def setUp(self):
        self.program = {
            "device_model_id": 9, "power": 0, "program_preset": 1, "preset": 2,
            "mode": 1, "program_v1": 50, "program_v2": 80, "program_t1": 30,
            "program_t2": 50,
        }

    def test_syncra_uses_program_speed_even_when_power_is_zero(self):
        self.assertEqual(speed_percent(self.program), 50)
        self.assertEqual(speed_command(self.program, 55), (
            "/v2/program",
            {"program_preset": 1, "program": 2, "mode": 1, "v1": 55, "v2": 80,
             "t1": 3.0, "t2": 5.0, "start": 0},
            55,
        ))
        self.assertEqual(self.program["program_v1"], 50)

    def test_upper_slider_preserves_the_minimum(self):
        device = {**self.program, "device_model_id": 6, "preset": 1}
        self.assertEqual(speed_percent(device), 80)
        self.assertEqual(speed_command(device, 70)[1]["v1"], 50)
        self.assertEqual(speed_command(device, 70)[1]["v2"], 70)
        with self.assertRaises(ValueError):
            speed_command(device, 52)

    def test_legacy_uses_status_and_quantizes_to_the_app_steps(self):
        device = {"device_model_id": 5, "power": 48, "power_switch": True}
        self.assertEqual(speed_percent(device), 48)
        self.assertEqual(speed_command(device, 50), (
            "/status", {**device, "power": 48, "updating": True}, 48,
        ))

    def test_missing_or_unrecognized_speed_does_not_expose_power(self):
        self.assertIsNone(speed_percent({"device_model_id": 7, "power": 0}))
        self.assertIsNone(speed_percent({"device_model_id": 9, "power": 0}))
        with self.assertRaises(ValueError):
            speed_command({**self.program, "program_t1": None}, 55)
