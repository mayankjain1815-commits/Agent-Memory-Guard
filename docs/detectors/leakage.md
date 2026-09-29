# Sensitive Data Leakage Detector

Detects when sensitive data (API keys, passwords, PII, credentials) is being written to agent memory, which could lead to data exfiltration or unintended exposure.

## Threat Description

AI agents may inadvertently store sensitive information in persistent memory — API keys from tool outputs, user credentials, or PII from conversations. This data can then be leaked through memory retrieval, shared across sessions, or exposed via memory dumps.

**OWASP Reference:** ASI-06 (Memory Poisoning — data exfiltration vector)

## Detection Patterns

The detector identifies:

- API keys and tokens (AWS, GitHub, OpenAI, Stripe, etc.)
- Passwords and secrets in plaintext
- Credit card numbers (Luhn-validated)
- Social Security Numbers (SSN)
- Email addresses in bulk
- Private keys (RSA, SSH, PGP)
- Database connection strings with credentials
- JWT tokens

## Severity

| Data Type | Severity |
|-----------|----------|
| Private keys, database credentials | CRITICAL |
| API keys, tokens | HIGH |
| Credit cards, SSN | HIGH |
| Email addresses, phone numbers | MEDIUM |

## Example

```python
from agent_memory_guard import MemoryGuard, Policy

guard = MemoryGuard(policy=Policy.strict())

# Blocked — API key detected
guard.write("tool_result", "Response: sk-proj-abc123def456...")
# → Action.QUARANTINE

# Blocked — credit card
guard.write("user_data", "Card: 4532-1234-5678-9012")
# → Action.QUARANTINE

# Safe
guard.write("tool_result", "The weather in NYC is 72°F")
# → Action.ALLOW
```

## Custom Patterns

Add organization-specific patterns:

```python
from agent_memory_guard.detectors.leakage import SensitiveDataDetector

detector = SensitiveDataDetector(
    custom_patterns=[
        r"INTERNAL-\d{6}",           # Internal document IDs
        r"(?i)project\s+codename",   # Project codenames
    ]
)
```

## Remediation

When sensitive data is detected:

1. The value is quarantined (not written to memory)
2. A SecurityEvent is emitted for logging/alerting
3. Consider using a secrets manager instead of agent memory for credentials
