"""Small offline demonstration of local PACE route selection."""
from .routing import Link, Policy, Transport, route
from .telemetry import LinkSummary, environment_report, serialize_report


def main():
    links = [
        Link("mesh", Transport.LORA, True, True, True, True, 0, 68, 90, 95, 8),
        Link("hotel-wifi", Transport.WIFI, False, True, True, True, 0, 99, 80, 65, 4),
        Link("cell-data", Transport.CELLULAR, True, True, True, True, .1, 92, 45, 55, 3),
    ]
    policy = Policy()
    decision = route(links, policy, advisory_order=("hotel-wifi", "cell-data"))
    print("Selected authorized route:", decision.selected)
    print("Rejected:", decision.rejected)
    summaries = tuple(LinkSummary(x.kind.value, x.name in decision.eligible,
                                  "good" if x.quality >= 80 else "fair" if x.quality >= 50 else "poor")
                      for x in links)
    print("Redacted HQ preview (NOT uploaded):", serialize_report(environment_report(63, summaries)))


if __name__ == "__main__":
    main()
