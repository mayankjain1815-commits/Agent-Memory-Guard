# AutoGen Agent Memory Guard

[![PyPI](https://img.shields.io/pypi/v/autogen-agent-memory-guard)](https://pypi.org/project/autogen-agent-memory-guard/)
[![OWASP](https://img.shields.io/badge/OWASP-Agent%20Memory%20Guard-blue)](https://owasp.org/www-project-agent-memory-guard/)

Memory security middleware for [Microsoft AutoGen](https://github.com/microsoft/autogen) agents. Scans all messages for prompt injection, secret leakage, and memory poisoning attacks before they enter agent memory.

## Installation

```bash
pip install autogen-agent-memory-guard
```

## Quick Start

### Single Agent Protection

```python
from autogen_agent_memory_guard import GuardedConversableAgent

# Drop-in replacement for ConversableAgent
agent = GuardedConversableAgent(
    name="assistant",
    system_message="You are a helpful assistant.",
    llm_config={"model": "gpt-4o"},
    on_violation="strip",  # Options: block, warn, strip, quarantine
)

# Use exactly like a normal AutoGen agent
agent.initiate_chat(other_agent, message="Research AI trends")
```

### Multi-Agent Group Chat

```python
from autogen_agent_memory_guard import GuardedGroupChat
from autogen import ConversableAgent, GroupChatManager

researcher = ConversableAgent("researcher", llm_config=config)
writer = ConversableAgent("writer", llm_config=config)

# All messages scanned before entering shared history
chat = GuardedGroupChat(
    agents=[researcher, writer],
    on_violation="strip",
    max_round=15,
)

manager = GroupChatManager(groupchat=chat.group_chat)
researcher.initiate_chat(manager, message="Research memory attacks")
```

### Low-Level Hook API

```python
from autogen_agent_memory_guard import MemoryGuardHook
from agent_memory_guard import Policy

hook = MemoryGuardHook(
    policy=Policy.strict(),
    on_violation="block",
)

# Scan any message manually
result = hook.scan_message(
    content="Ignore all previous instructions...",
    sender="user_input",
    role="user",
)

print(result.allowed)    # False
print(result.violations) # [ViolationType.PROMPT_INJECTION]
```

## Detection Capabilities

| Layer | What It Catches | Latency |
|-------|----------------|---------|
| Entropy Analysis | Obfuscated payloads, base64 bombs | ~12µs |
| Heuristic Rules | Known injection patterns, role hijacking | ~8µs |
| Semantic Analysis | Context-aware manipulation attempts | ~35µs |
| Secret Detection | API keys, tokens, PII in messages | ~15µs |

## Violation Handling Modes

- **block**: Reject the message entirely (default)
- **warn**: Allow but log a warning with full violation details
- **strip**: Remove malicious content, pass sanitized message through
- **quarantine**: Store in quarantine log for manual review

## Metrics & Observability

```python
# Get scan statistics
metrics = agent.metrics
print(f"Messages scanned: {metrics['total_scanned']}")
print(f"Violations found: {metrics['violations_found']}")
print(f"Avg latency: {metrics['avg_latency_us']}µs")
```

## Compatibility

- AutoGen v0.2.x (pyautogen)
- AutoGen v0.4.x (autogen-agentchat)
- Python 3.9+

## Links

- [OWASP Project Page](https://owasp.org/www-project-agent-memory-guard/)
- [Core Library (agent-memory-guard)](https://pypi.org/project/agent-memory-guard/)
- [LangChain Integration](https://pypi.org/project/langchain-agent-memory-guard/)
- [GitHub Repository](https://github.com/OWASP/www-project-agent-memory-guard)
