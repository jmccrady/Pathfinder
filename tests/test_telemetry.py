import json
import pytest
from pathfinder.telemetry import LinkSummary, environment_report, serialize_report


def test_report_excludes_location_identity_and_raw_radio_data():
    raw = serialize_report(environment_report(63, (LinkSummary("lora", True, "good"),)))
    assert json.loads(raw)["battery_bucket"] == "50-75"
    for forbidden in ("latitude", "longitude", "imsi", "imei", "mac", "serial", "message", "raw_rf"):
        assert forbidden not in raw.lower()


def test_rogue_report_field_rejected():
    report = environment_report(40, ())
    report["latitude"] = 39.0
    with pytest.raises(ValueError):
        serialize_report(report)


def test_rogue_link_field_rejected():
    report = environment_report(40, (LinkSummary("lora", True, "good"),))
    report["links"][0]["peer_id"] = "secret"
    with pytest.raises(ValueError):
        serialize_report(report)


def test_invalid_input_rejected():
    with pytest.raises(ValueError):
        environment_report(101, ())
    with pytest.raises(ValueError):
        LinkSummary("unknown-radio", True, "good")
