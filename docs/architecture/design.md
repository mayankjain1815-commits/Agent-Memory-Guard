# Architecture

## Design Principles

Agent Memory Guard is built on four core principles:

1. **Defense in Depth** — Multiple independent detectors, each specializing in a different threat class
2. **Minimal Overhead** — Rule-based detectors add <1ms per operation; ML detection is optional
3. **Framework Agnostic** — Works with any memory store via the `MemoryStore` interface
4. **Fail-Safe Defaults** — Permissive by default (detect + log), strict mode opt-in

## Component Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         MemoryGuard                              │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐│
│  │  Detectors  │  │   Policy    │  │    Event Handlers       ││
│  │             │  │   Engine    │  │                         ││
│  │ • Injection │  │             │  │ • Logging               ││
│  │ • Leakage   │  │ • Permissive│  │ • Alerting              ││
│  │ • Priv Esc  │  │ • Strict    │  │ • Metrics               ││
│  │ • Tool Abuse│  │ • Tiered    │  │ • Custom callbacks      ││
│  │ • Autonomy  │  │ • Custom    │  │                         ││
│  │ • Cross-Task│  │             │  │                         ││
│  │ • Self-Reinf│  │             │  │                         ││
│  │ • ML (opt)  │  │             │  │                         ││
│  │ • Anomaly   │  │             │  │                         ││
│  └─────────────┘  └─────────────┘  └─────────────────────────┘│
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐│
│  │  Integrity  │  │  Snapshots  │  │   Classification        ││
│  │  Registry   │  │   Store     │  │   Registry              ││
│  └─────────────┘  └─────────────┘  └─────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
         │                                        │
         ▼                                        ▼
┌─────────────────┐                    ┌─────────────────────┐
│  Memory Store   │                    │  Security Events    │
│  (pluggable)    │                    │  (structured logs)  │
└─────────────────┘                    └─────────────────────┘
```

## Request Flow

### Write Operation

```
guard.write(key, value, source)
    │
    ├─► Classification: Determine memory class (system/user/tool)
    │
    ├─► Integrity Check: Verify hash if key exists
    │
    ├─► Detector Pipeline (sequential):
    │   ├─► ProtectedKeyDetector
    │   ├─► PromptInjectionDetector
    │   ├─► SensitiveDataDetector
    │   ├─► PrivilegeEscalationDetector
    │   ├─► ToolAbuseDetector
    │   ├─► ExcessiveAutonomyDetector
    │   ├─► CrossTaskContaminationDetector
    │   ├─► SelfReinforcementDetector
    │   ├─► SizeAnomalyDetector
    │   ├─► RapidChangeDetector
    │   └─► MLInjectionDetector (if installed)
    │
    ├─► Policy Decision: allow / quarantine / block
    │
    ├─► Event Emission: SecurityEvent → handlers
    │
    ├─► Snapshot (if blocked + snapshot_on_block=True)
    │
    └─► Store Write (if allowed) or Quarantine
```

### Read Operation

```
guard.read(key)
    │
    ├─► Check quarantine status
    ├─► Integrity verification
    └─► Return value (or None if quarantined)
```

## Memory Store Interface

AMG works with any backend that implements the `MemoryStore` protocol:

```python
class MemoryStore(Protocol):
    def get(self, key: str) -> Any | None: ...
    def set(self, key: str, value: Any) -> None: ...
    def delete(self, key: str) -> None: ...
    def keys(self) -> list[str]: ...
```

Built-in implementations:

- `InMemoryStore` — dict-based (default, for testing)
- Custom stores can wrap Redis, PostgreSQL, DynamoDB, etc.

## Snapshot System

When a write is blocked, AMG can automatically snapshot the memory state before the block. This enables:

- Forensic analysis of attack attempts
- Rollback to known-good state
- Audit trail for compliance

## Classification System

Memory entries are classified into tiers:

| Class | Description | Protection Level |
|-------|-------------|-----------------|
| SYSTEM | Agent instructions, prompts | Highest — immutable |
| TOOL | Tool outputs, API responses | High — validated |
| USER | User preferences, context | Medium — screened |
| EPHEMERAL | Temporary, session-scoped | Low — basic checks |

Classification determines which detectors run and how strict the policy enforcement is.
