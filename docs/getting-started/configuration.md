# Configuration

Agent Memory Guard can be configured via Python code, YAML policy files, or environment variables.

## Python Configuration

```python
from agent_memory_guard import MemoryGuard, Policy

guard = MemoryGuard(
    policy=Policy.strict(),
    snapshot_on_block=True,       # Auto-snapshot before blocking
    current_task="task_123",      # Enable cross-task detection
)
```

## YAML Policy Files

Create a `.amg-policy.yml` file in your project root:

```yaml
version: "1"
policy: strict

protected_keys:
  - system_prompt
  - agent_instructions
  - tool_permissions
  - security_config

detectors:
  prompt_injection:
    enabled: true
    severity_threshold: medium
  sensitive_data:
    enabled: true
    patterns:
      - "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b"
      - "\\b\\d{3}-\\d{2}-\\d{4}\\b"
  privilege_escalation:
    enabled: true
  tool_abuse:
    enabled: true
  excessive_autonomy:
    enabled: true

actions:
  on_critical: quarantine
  on_high: quarantine
  on_medium: log
  on_low: allow
```

Load a policy file:

```python
policy = Policy.from_yaml(".amg-policy.yml")
guard = MemoryGuard(policy=policy)
```

## Environment Variables

The API server (`amg serve`) reads these environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `AMG_POLICY` | `strict` | Policy mode: `permissive`, `strict`, `tiered` |
| `AMG_HOST` | `0.0.0.0` | Server bind address |
| `AMG_PORT` | `8000` | Server port |
| `AMG_LOG_LEVEL` | `info` | Logging level |
| `AMG_CORS_ORIGINS` | `*` | Allowed CORS origins (comma-separated) |

## Detector Configuration

Each detector can be individually enabled/disabled and configured:

```python
from agent_memory_guard.detectors.injection import PromptInjectionDetector
from agent_memory_guard.detectors.leakage import SensitiveDataDetector

guard = MemoryGuard(
    detectors=[
        PromptInjectionDetector(),
        SensitiveDataDetector(custom_patterns=[r"INTERNAL-\d+"]),
    ]
)
```

## Logging

AMG uses Python's standard `logging` module under the `agent_memory_guard` logger:

```python
import logging
logging.getLogger("agent_memory_guard").setLevel(logging.DEBUG)
```
