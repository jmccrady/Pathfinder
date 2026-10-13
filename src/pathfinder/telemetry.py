"""Privacy-minimizing Communications Environment Report serialization."""
from __future__ import annotations
from dataclasses import dataclass
import json
import secrets

ALLOWED_KINDS = frozenset({"lora", "wifi", "cellular", "satellite"})
ALLOWED_QUALITIES = frozenset({"poor", "fair", "good", "unknown"})


@dataclass(frozen=True)
class LinkSummary:
    kind: str
    eligible: bool
    quality: str

    def __post_init__(self):
        if self.kind not in ALLOWED_KINDS or self.quality not in ALLOWED_QUALITIES:
            raise ValueError("invalid link summary")


def environment_report(battery_percent: int, links: tuple[LinkSummary, ...]) -> dict:
    if not 0 <= battery_percent <= 100:
        raise ValueError("battery percent out of range")
    bucket = "0-25" if battery_percent < 25 else "25-50" if battery_percent < 50 else "50-75" if battery_percent < 75 else "75-100"
    return {
        "schema": "pf.cer.v1",
        "request_nonce": secrets.token_hex(12),
        "battery_bucket": bucket,
        "links": [{"kind": x.kind, "eligible": x.eligible, "quality": x.quality} for x in links]
    }


def serialize_report(report: dict) -> str:
    """Strict schema rejection, including unknown fields potentially containing PII."""
    if set(report) != {"schema", "request_nonce", "battery_bucket", "links"}:
        raise ValueError("unknown or missing report fields")
    if report["schema"] != "pf.cer.v1":
        raise ValueError("wrong report schema")
    if not isinstance(report["request_nonce"], str) or len(report["request_nonce"]) != 24:
        raise ValueError("invalid nonce")
    if report["battery_bucket"] not in {"0-25", "25-50", "50-75", "75-100"}:
        raise ValueError("invalid battery bucket")
    if not isinstance(report["links"], list):
        raise ValueError("invalid links")
    for item in report["links"]:
        if not isinstance(item, dict) or set(item) != {"kind", "eligible", "quality"}:
            raise ValueError("unknown link fields")
        if item["kind"] not in ALLOWED_KINDS or type(item["eligible"]) is not bool or item["quality"] not in ALLOWED_QUALITIES:
            raise ValueError("invalid link value")
    return json.dumps(report, sort_keys=True, separators=(",", ":"))
