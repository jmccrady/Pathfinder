"""Deterministic, authorization-first route selection; not an RF controller."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class Transport(str, Enum):
    LORA = "lora"
    WIFI = "wifi"
    CELLULAR = "cellular"


@dataclass(frozen=True)
class Link:
    name: str
    kind: Transport
    authorized: bool
    available: bool
    encrypted: bool
    legal: bool
    cost_per_mb: float
    quality: int
    energy: int
    privacy: int
    observed_age_s: int | None

    def __post_init__(self):
        for name in ("quality", "energy", "privacy"):
            if not 0 <= getattr(self, name) <= 100:
                raise ValueError(f"{name} must be in range 0..100")
        if self.cost_per_mb < 0:
            raise ValueError("cost_per_mb cannot be negative")
        if self.observed_age_s is not None and self.observed_age_s < 0:
            raise ValueError("observation age cannot be negative")


@dataclass(frozen=True)
class Policy:
    max_cost_per_mb: float = 0.0
    max_observation_age_s: int = 120
    min_privacy: int = 50
    require_encryption: bool = True


@dataclass(frozen=True)
class Decision:
    selected: str | None
    eligible: tuple[str, ...]
    rejected: dict[str, tuple[str, ...]]
    scores: dict[str, float]


def reasons(link: Link, policy: Policy) -> tuple[str, ...]:
    failures = []
    if not link.authorized:
        failures.append("unauthorized")
    if not link.available:
        failures.append("unavailable")
    if not link.legal:
        failures.append("noncompliant")
    if policy.require_encryption and not link.encrypted:
        failures.append("unencrypted")
    if link.cost_per_mb > policy.max_cost_per_mb:
        failures.append("cost_exceeded")
    if link.privacy < policy.min_privacy:
        failures.append("privacy_below_floor")
    if link.observed_age_s is None or link.observed_age_s > policy.max_observation_age_s:
        failures.append("stale_or_missing_observation")
    return tuple(failures)


def route(links: Iterable[Link], policy: Policy = Policy(),
          advisory_order: tuple[str, ...] = ()) -> Decision:
    """Cloud advice is advisory only; it cannot change eligibility."""
    candidates = list(links)
    if len({link.name for link in candidates}) != len(candidates):
        raise ValueError("link names must be unique")
    rejected = {link.name: reasons(link, policy) for link in candidates}
    eligible = [link for link in candidates if not rejected[link.name]]
    # Trustworthiness is a hard gate. Ranking uses quality, energy and privacy.
    scores = {link.name: round(link.quality * .5 + link.energy * .2 + link.privacy * .3, 2)
              for link in eligible}
    advice = {name: i for i, name in enumerate(advisory_order)}
    eligible.sort(key=lambda link: (-scores[link.name], advice.get(link.name, 10**9), link.name))
    return Decision(selected=eligible[0].name if eligible else None,
                    eligible=tuple(link.name for link in eligible),
                    rejected={name: flags for name, flags in rejected.items() if flags},
                    scores=scores)
