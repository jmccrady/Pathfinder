import pytest
from pathfinder.routing import Link, Policy, Transport, route


def link(name="mesh", **overrides):
    values = dict(name=name, kind=Transport.LORA, authorized=True, available=True,
                  encrypted=True, legal=True, cost_per_mb=0, quality=70,
                  energy=80, privacy=90, observed_age_s=4)
    values.update(overrides)
    return Link(**values)


def test_authorization_precedes_quality_or_advice():
    result = route([link(), link("rogue", authorized=False, quality=100)],
                   advisory_order=("rogue",))
    assert result.selected == "mesh"
    assert "unauthorized" in result.rejected["rogue"]


def test_disallows_noncompliant_unencrypted_and_expensive():
    bad = link("bad", legal=False, encrypted=False, cost_per_mb=2)
    result = route([bad], Policy(max_cost_per_mb=0))
    assert result.selected is None
    assert set(result.rejected["bad"]) >= {"noncompliant", "unencrypted", "cost_exceeded"}


def test_stale_link_rejected():
    assert route([link(observed_age_s=121)]).selected is None
    assert route([link(observed_age_s=None)]).selected is None


def test_deterministic_tiebreak():
    assert route([link("z"), link("a")]).selected == "a"


def test_duplicate_names_rejected():
    with pytest.raises(ValueError):
        route([link("same"), link("same")])


def test_invalid_quality_rejected():
    with pytest.raises(ValueError):
        link(quality=101)


def test_advice_cannot_override_privacy_floor():
    result = route([link("leaky", privacy=0), link("private")], advisory_order=("leaky",))
    assert result.selected == "private"
