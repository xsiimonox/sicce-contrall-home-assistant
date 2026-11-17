"""Unit tests for protocol-independent Sicce response handling."""
from custom_components.sicce_contrall.api import SicceClient
from custom_components.sicce_contrall.coordinator import device_id


def test_extract_devices_from_common_api_envelopes():
    assert SicceClient._devices({"devices": [{"id": 1}]}) == [{"id": 1}]
    assert SicceClient._devices({"data": [{"device_id": "abc"}]}) == [{"device_id": "abc"}]
    assert SicceClient._devices({"id": 7, "name": "Pump"}) == [{"id": 7, "name": "Pump"}]


def test_device_id_prefers_the_cloud_id():
    assert device_id({"id": 3, "mac": "aa:bb"}) == "3"
    assert device_id({"device_id": "controller-1"}) == "controller-1"
    assert device_id({"name": "unnamed"}) is None


def test_login_token_can_be_nested_or_flat():
    assert SicceClient._token_from_login({"token": "flat"}) == "flat"
    assert SicceClient._token_from_login({"result": True, "data": {"access_token": "nested"}}) == "nested"
    assert SicceClient._token_from_login({"result": False, "error": "INVALID_USER_OR_PASSWORD"}) is None
