# Secure Agent Starter Template

A minimal, production-ready template for building AI agents with memory security built in from day one.

## What's included

```
your-agent/
├── agent.py              # Agent with AMG-protected memory
├── policy.yaml           # Declarative security policy
├── requirements.txt      # Dependencies (agent-memory-guard pinned)
├── tests/
│   └── test_memory.py    # Verify your guard catches attacks
└── README.md
```

## Quick start

```bash
# Clone this template
git clone https://github.com/OWASP/www-project-agent-memory-guard
cp -r templates/secure-agent-starter my-agent
cd my-agent

# Install
pip install -r requirements.txt

# Run the agent
python agent.py

# Run security tests
pytest tests/
```

## What you get for free

- **Prompt injection detection** on every memory write
- **Secret/PII redaction** before storage
- **Protected key enforcement** — agent identity can't be overwritten
- **Size anomaly detection** — blocks buffer overflow attempts
- **Audit trail** — every decision logged as a structured SecurityEvent
- **Rollback** — point-in-time snapshots for recovery

## Customize the policy

Edit `policy.yaml` to match your threat model:

```yaml
version: 1
default_action: allow
protected_keys: [system.*, identity.*, agent.goal]
immutable_keys: [identity.user_id]

rules:
  - { name: block_injection, on: prompt_injection, action: block }
  - { name: redact_secrets,  on: sensitive_data,   action: redact }
  - { name: block_protected, on: protected_key,    action: block }
  - { name: quarantine_size, on: size_anomaly,     action: quarantine }
```

## Next steps

- Add your LLM integration (OpenAI, Anthropic, etc.)
- Connect a persistent backend (Redis, PostgreSQL)
- Add the LangChain middleware: `pip install langchain-agent-memory-guard`
- Set up OpenTelemetry export for production monitoring

## References

- [OWASP Agent Memory Guard](https://github.com/OWASP/www-project-agent-memory-guard)
- [OWASP ASI06: Memory Poisoning](https://owasp.org/www-project-top-10-for-llm-applications/)
