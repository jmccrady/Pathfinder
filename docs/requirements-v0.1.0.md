# Pathfinder System Requirements Specification (PF-SRS-001)
Version: **0.1.0** | Date: **2026-10-13** | Status: **Draft baseline**

## Mission
Pathfinder is a standalone, privacy-first adaptive communications handheld. PACE (Pathfinder Adaptive Communications Engine) measures supported local link conditions, ranks **authorized** transports, queues encrypted messages, and optionally asks a cloud AI for schema-limited advisory recommendations. Core routing never depends on the cloud.

## Architectural decisions
- **ADR-001 — Telemetry minimization.** HQ receives no GNSS coordinates, real-world identifiers, address book, peer graph, message contents, raw radio capture, or persistent hardware IDs by default. Advisory input uses an explicit allowlist, coarse link and battery classes, ephemeral request nonce, and no diagnostics logging of payloads.
- **ADR-002 — Hybrid intelligence.** Deterministic local policy gates authorization, cost limits, regulatory constraints, permissions and encryption *before* scoring. HQ AI suggestions are optional, time-bound, authenticated and never directly execute radio commands or override the local policy.
- **ADR-003 — Protection.** Authenticated **local** cryptographic erasure of keys protecting sensitive storage plus a separate privacy-stop button that halts application location sharing and HQ uploads. Physical destruction and AI-initiated erasure are excluded.

## Safety, privacy and scope
Permitted transports include provisioned LoRa mesh, authorized Wi-Fi/IP gateways, optionally subscribed cellular and separately assessed satellite paths. Receive-only spectrum observation may estimate occupancy but MUST NOT intercept protected third-party content or treat discovered networks as authorization to transmit. Cellular network operators may observe subscriber, signaling and location-related metadata even when application data is encrypted. Do not claim covert or anonymous cellular operation, global reach, guaranteed SOS delivery or guaranteed erasure of already-transmitted data. This is not an emergency locator beacon.

## Testable functional requirements
| ID | Priority | Requirement | Acceptance test |
| --- | --- | --- | --- |
| PF-FR-001 | Must | Keyboard, display, messaging status and device settings function without a phone or HQ. | Disconnect external networks and complete core on-device workflow. |
| PF-FR-002 | Must | Transport abstraction supports capabilities, state, send and delivery result. | Mock LoRa, Wi-Fi and unavailable adapters pass shared contract tests. |
| PF-FR-003 | Must | Local policy filters by authorization, privacy, encryption, regulations, cost and availability before ranking. | Ineligible high-score link is never selected. |
| PF-FR-004 | Must | Durable store-and-forward queue provides message ID, retry with backoff, TTL, dedupe and terminal status. | Interrupted connection/restored connection delivers only once and expires stale data. |
| PF-FR-005 | Must | Observation engine reports signal quality and freshness, with unavailable values marked unknown. | Stale samples excluded from current route decisions. |
| PF-FR-006 | Must | Redacted Communications Environment Report (CER) schema excludes precise location and identifiers by default. | Serialization/schema and log-inspection negative tests reject prohibited fields. |
| PF-FR-007 | Must | Optional HQ advisory returns versioned candidate preferences, reason and expiry. | Invalid, replayed and expired replies rejected. |
| PF-FR-008 | Must | Cloud AI cannot run system commands, invoke erasure, disclose secrets or alter transport authorization. | Adversarial recommendation tests prove local policy supremacy. |
| PF-FR-009 | Must | Device-to-device application messages are encrypted and authenticated independent of relays; keys are provisioned securely. | Third-party gateway cannot decrypt or forge messages; replay rejected. |
| PF-FR-010 | Must | Location sharing requires explicit time-limited per-peer consent and supports revoke. | Fresh device shares no position, expired or revoked grants stop updates. |
| PF-FR-011 | Must | Immediate privacy stop disables app location transmissions and HQ advisory uploads until locally re-enabled. | Network trace shows no further application disclosures; interface shows current state. |
| PF-FR-012 | Must | Local Zeroize requires operator authentication and confirmation, erases appropriate data-encryption keys and verifies results. | Post-zeroize storage cannot be decrypted with remaining local key material; failures clearly reported. |
| PF-FR-013 | Must | Offline operation tolerates link loss, HQ outage, bad clocks and low battery. | Fault-injection suite produces safe degradation. |
| PF-FR-014 | Should | Spectrum awareness is receive-only, aggregated and limited to permitted measurement methods. | RF observations omit recovered third-party content. |
| PF-FR-015 | Should | Navigation shows GNSS position, bearing, straight-line distance, relative altitude and data age. | Known geodesic fixtures pass; stale positions clearly marked. |
| PF-FR-016 | Should | Optional authorized cellular adapter supports explicit cost limits and connection lifecycle. | Unprovisioned service never eligible; metadata warning shown. |
| PF-FR-017 | Should | Signed firmware/configuration with rollback and recovery protections. | Modified image rejected; interrupted update recoverable. |
| PF-FR-018 | Could | Gateway/satellite adapters integrate without bypassing policy. | Simulation uses new adapter and keeps all security invariants. |

## Nonfunctional and security requirements
- **PF-NFR-001:** No subscription for local routing/mesh; optional transport plans may incur fees.
- **PF-NFR-002:** Encrypt sensitive local stores; evaluate hardware-backed key storage; no plaintext secrets in logs.
- **PF-NFR-003:** Default no HQ analytics; document endpoint IP and server log implications, and retention policies.
- **PF-NFR-004:** Fuzz untrusted RF, transport payloads, status reports and AI outputs.
- **PF-NFR-005:** Critical security decisions deterministic and unit-testable.
- **PF-NFR-006:** Surface selected route, rationale, uncertainty, report age and privacy indicator.
- **PF-NFR-007:** Region-specific RF parameters and properly authorized transmitters.
- **PF-NFR-008:** Document carrier signaling limits, radio range limitations, and erasure boundaries.
- **PF-NFR-009:** Size, power endurance and link throughput claims are test results, not initial guarantees.

## Trust boundaries
```text
sensors & provisioned transport adapters -> normalized observations
 -> deterministic local eligibility gate -> route selection -> encrypted queue -> approved transport -> peer
                  |
             redaction allowlist
                  |  OPTIONAL
                  v
           authenticated HQ API -> constrained AI advisory
                  |
           validate schema, expiry, origin -> local policy re-check
```
HQ cannot request raw identifiers or RF intercepts. Advice names only transport candidates reported by the device, never frequencies, shell commands or credentials.

## CER sample — illustration only
```json
{
  "schema": "pf.cer.v1",
  "request_nonce": "short-lived-random-token",
  "battery_bucket": "50-75",
  "links": [
    {"kind":"lora","eligible":true,"quality":"fair","age_bucket":"0-30s"},
    {"kind":"wifi","eligible":false,"quality":"unknown","age_bucket":"unknown"}
  ]
}
```

## State machines
- **Message:** QUEUED -> IN_FLIGHT -> DELIVERED / RETRY / FAILED / EXPIRED; bounded retries and deduplication.
- **Advisory:** IDLE -> REDACTED -> SENT -> VALIDATED -> RECHECKED -> APPLIED / REJECTED.
- **Privacy:** NORMAL -> STOPPED -> NORMAL only after an explicit authenticated local action.
- **Zeroize:** LOCKED -> AUTHENTICATED -> CONFIRMED -> ERASING_KEYS -> VERIFIED / FAILURE. Protected keys must not remain in backups or removable media.

## Release gates
- **Gate A:** deterministic simulator, mock transports, schema redaction and local enforcement tests pass.
- **Gate B:** privacy stop, cryptography, consent and erasure receive security test evidence.
- **Gate C:** live hardware tests for radio legality, battery, GNSS, UI and fault recovery.
- **Gate D:** release documentation discloses metadata, range, satellite and SOS limitations.

## Open decisions
Linux host versus MCU-only; Meshtastic upstream integration mode; secure element and key hierarchy; exact E2EE protocol and cryptographic libraries; offline map format; data retention period; chosen regulatory regions; firmware licensing; real hardware and energy budgets.

## Change control
Requirement IDs are stable. Any modified requirement needs rationale, corresponding tests and changelog revision. Versions 0.x are experimental drafts; 1.0 requires review and approval.

### Changelog
- **0.1.0 — 2026-10-13:** Initial PACE requirements baseline from three approved principles: minimum telemetry, hybrid AI and authenticated cryptographic erase/privacy stop.
