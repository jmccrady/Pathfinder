# Pathfinder Implementation Backlog (PF-BL-001)
Version **0.1.0** | Date **2026-10-13** | State **Proposed**  
Based on [PF-SRS-001 v0.1.0](requirements-v0.1.0.md). Estimates are planning sizes, not delivery promises.

**Priority:** P0 foundation, P1 first physical prototype, P2 later capability. **Size:** S small, M medium, L large.

| Task | Priority | Size | Depends on | Deliverable / definition of acceptance | Requirements |
| --- | --- | --- | --- | --- | --- |
| PF-001 | P0 | S | — | Repository scaffold, project conventions, CI and repeatable test entrypoint. | NFR-005 |
| PF-002 | P0 | M | PF-001 | Threat model, data inventory, disclosure map and explicitly documented carrier metadata limitation. | FR-006, FR-009, FR-012 |
| PF-003 | P0 | M | PF-001 | Pluggable adapter interface with MockLoRa, MockWiFi, MockCellular and unavailable link state; contract tests. | FR-002, FR-005 |
| PF-004 | P0 | M | PF-002/003 | Authorization-first deterministic eligibility/ranking engine with reproducible policy tests. | FR-003, FR-008 |
| PF-005 | P0 | M | PF-003 | Encrypted store-and-forward queue: IDs, TTL, bounded backoff, dedupe and restart test. | FR-004, FR-013 |
| PF-006 | P0 | S | PF-002 | Strict CER schema and redaction allowlist; forbidden keys blocked at serializer and log boundary. | FR-006 |
| PF-007 | P0 | M | PF-004/006 | Optional mock HQ with authenticated, expiring, schema-limited recommendations and local recheck. | FR-007/008 |
| PF-008 | P0 | M | PF-004/005/007 | Multi-link simulator with outages, intermittent HQ, latency, cost, packet loss and energy model; compare AI vs non-AI decisions. | FR-013, NFR-005 |
| PF-009 | P1 | L | PF-002 | Secure peer pairing and reviewed E2EE implementation, message authentication and replay defense. | FR-009 |
| PF-010 | P1 | M | PF-009 | Per-peer tracking consent, lease expiration and revocation tests. | FR-010 |
| PF-011 | P1 | M | PF-006/010 | Privacy-stop workflow, visible on-device status and packet-capture negative tests. | FR-011 |
| PF-012 | P1 | L | PF-002/009 | Local authenticated Zeroize prototype, key-erasure verification, forensic tests and failure status. | FR-012 |
| PF-013 | P1 | L | PF-003/005/009 | Supported Meshtastic LoRa adapter, lawful region settings and peer-to-peer hardware validation. | FR-001/002/009 |
| PF-014 | P1 | M | PF-003/006 | Authorized Wi-Fi/gateway adapter, private transport configuration and disconnection tests. | FR-002/006 |
| PF-015 | P1 | L | PF-004/010 | Keyboard UI for inbox, link ranking, route reasoning, privacy, tracking and navigation. | FR-001/015 |
| PF-016 | P2 | M | PF-002/003 | Receive-only spectrum summary plug-in, without interception storage or transmit access. | FR-014 |
| PF-017 | P2 | L | PF-006/014 | Explicitly provisioned cellular link with cost policy, warning, session lifecycle and trace audit. | FR-016 |
| PF-018 | P2 | L | PF-012/015 | Protected key storage, boot verification, signed updates and recovery. | FR-017 |
| PF-019 | P2 | M | PF-008/017 | Satellite feasibility study, coverage/cost and lawful gateway candidates; mock adapter only. | FR-018 |
| PF-020 | P1 | M | PF-008/011/012 | Security test campaign: outages, prompt injection, privacy logs, key erasure and policy bypass attempts. | Gates A-D |

## Releases
- **R0 — PACE simulator:** PF-001 through PF-008. Core demo demonstrates authorized routing, offline queues, no location in HQ reports, rejection of malicious advice.
- **R1 — Trusted handheld:** PF-009 through PF-015 and PF-020. Physical mesh/Wi-Fi, on-device user experience, privacy stop, consent and erasure with evidence.
- **R2 — Extended transports:** PF-016 through PF-019. SDR receive-only awareness, optional provisioned cellular and gateway feasibility.

## Acceptance criteria for every task
Code reviewed; repeatable tests pass; errors and edge cases documented; traceability to PF-SRS maintained; security/privacy regression checks added; simulator claims separated from hardware measurements.

## Immediate sprint
1. PF-001 initialize scaffold and CI.
2. PF-002 threat model and authorized-links inventory.
3. PF-003 adapter contracts and test doubles.
4. PF-006 strict schema with tests; default no GNSS or identity to HQ.
5. PF-004 prove unauthorized link cannot win route scoring.

## Deferred and explicitly excluded
No physical self-destruct, unauthorized cellular entry, cryptographic backdoors, AI-controlled erasure, unrestricted SDR transmissions, or promises of anonymity against carriers.
