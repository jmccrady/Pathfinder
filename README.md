# Pathfinder
**Adaptive Communications Intelligence — PACE**

Pathfinder is an experimental privacy-first standalone communicator and transport-routing platform. It selects among **authorized** local mesh, Wi-Fi, provisioned cellular and future gateway paths. Local policy and queued messaging work offline; an optional HQ AI service can recommend, but never command, network choices.

## Baseline
- **Requirements:** [PF-SRS-001 v0.1.0](docs/requirements-v0.1.0.md)
- **Backlog:** [PF-BL-001 v0.1.0](docs/backlog-v0.1.0.md)
- **Current phase:** Specifications only; no functional firmware or validated privacy claims yet.

## Immutable design priorities
1. Minimal app telemetry; **no location to HQ by default**.
2. Offline deterministic routing; cloud AI advisory is optional and non-authoritative.
3. Authenticated local cryptographic erasure and separate emergency privacy stop.
4. Transmit only over authorized links. Passive spectrum sensing does not permit use of a discovered network.
5. Commercial cellular/satellite may incur service fees and necessarily expose some metadata to network operators.

## First release objective
Build a simulator with pluggable adapters, deterministic routing, a secure store-and-forward queue, a schema-limited Communications Environment Report and mocked HQ recommendations. Test failures and privacy invariants before adding radios.

This project is not a certified emergency rescue device and cannot guarantee anonymous or worldwide communications.

## Contributing
See the backlog and requirements before proposing changes. No unreviewed AI-to-hardware control paths, destructive hardware functions or unauthorized-network capabilities.
