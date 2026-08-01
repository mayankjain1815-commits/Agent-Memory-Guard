# Detectors

Agent Memory Guard uses a modular detector architecture. Each detector specializes in identifying a specific class of memory security threat. Detectors run in sequence on every memory write operation and return findings with severity levels.

## Available Detectors

| Detector | Threat Category | Severity Range | OWASP ID |
|----------|----------------|----------------|----------|
| [Prompt Injection](injection.md) | Instruction hijacking | HIGH–CRITICAL | ASI-03 |
| [Sensitive Data Leakage](leakage.md) | Data exfiltration | MEDIUM–HIGH | ASI-06 |
| [Privilege Escalation](privilege-escalation.md) | Unauthorized access | HIGH–CRITICAL | ASI-04 |
| [Tool Abuse](tool-abuse.md) | Dangerous tool invocation | MEDIUM–CRITICAL | ASI-07 |
| [Excessive Autonomy](excessive-autonomy.md) | Agent overreach | MEDIUM–HIGH | ASI-09 |
| [Cross-Task Contamination](cross-task.md) | Task boundary violation | MEDIUM–HIGH | ASI-06 |
| [Self-Reinforcement](self-reinforcement.md) | Feedback loop manipulation | MEDIUM–HIGH | ASI-06 |
| [ML-Based Detection](ml-detection.md) | Advanced injection (DistilBERT) | HIGH–CRITICAL | ASI-03 |
| Size Anomaly | Unusually large values | LOW–MEDIUM | ASI-06 |
| Rapid Change | Suspicious write frequency | LOW–MEDIUM | ASI-06 |

## How Detectors Work

Each detector implements the `Detector` interface:

```python
from agent_memory_guard.detectors.base import Detector, DetectionResult

class MyDetector(Detector):
    def detect(self, key: str, value: any, **context) -> DetectionResult:
        # Analyze the key-value pair
        # Return DetectionResult with is_threat, severity, message
        ...
```

## Severity Levels

| Level | Meaning | Default Action (Strict) |
|-------|---------|------------------------|
| CRITICAL | Immediate security risk | Block/Quarantine |
| HIGH | Likely attack attempt | Block/Quarantine |
| MEDIUM | Suspicious pattern | Log + Alert |
| LOW | Minor anomaly | Log |
| INFO | Informational | Allow |

## Enabling/Disabling Detectors

By default, all rule-based detectors are enabled. The ML detector requires the `ml` extra.

```python
from agent_memory_guard import MemoryGuard
from agent_memory_guard.detectors.injection import PromptInjectionDetector
from agent_memory_guard.detectors.leakage import SensitiveDataDetector

# Use only specific detectors
guard = MemoryGuard(detectors=[
    PromptInjectionDetector(),
    SensitiveDataDetector(),
])
```

## Custom Detectors

You can create custom detectors by implementing the `Detector` base class:

```python
from agent_memory_guard.detectors.base import Detector, DetectionResult

class CompanyPolicyDetector(Detector):
    """Detect violations of company-specific memory policies."""

    name = "CompanyPolicyDetector"

    def detect(self, key: str, value: any, **context) -> DetectionResult:
        if "CONFIDENTIAL" in str(value).upper():
            return DetectionResult(
                is_threat=True,
                detector=self.name,
                severity="high",
                message="Confidential data should not be stored in agent memory",
            )
        return DetectionResult(is_threat=False, detector=self.name)
```

Register it with the guard:

```python
guard = MemoryGuard(detectors=[
    *MemoryGuard.default_detectors(),
    CompanyPolicyDetector(),
])
```
