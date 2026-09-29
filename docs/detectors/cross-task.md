# Cross-Task Contamination Detector

Detects when memory from one task or session leaks into another, violating task isolation boundaries. This prevents one user's data or instructions from affecting another user's agent session.

## Threat Description

In multi-tenant or multi-task agent systems, memory should be isolated between tasks. Cross-task contamination occurs when:

- Data from Task A is written to Task B's memory space
- A shared memory store allows one session to influence another
- An attacker in one session poisons memory that affects other sessions

**OWASP Reference:** ASI-06 (Memory Poisoning — cross-task vector)

## How It Works

The detector tracks which task owns each memory key using the `current_task` parameter:

```python
guard = MemoryGuard(
    policy=Policy.strict(),
    current_task="task_123"
)
```

When a write occurs, the detector checks if the key was previously written by a different task. If so, it flags the operation as potential cross-task contamination.

## Severity

| Scenario | Severity |
|----------|----------|
| Overwriting another task's key | HIGH |
| Writing to a system-classified key from user context | HIGH |
| Reading cross-task data (informational) | MEDIUM |

## Example

```python
from agent_memory_guard import MemoryGuard, Policy

# Task A writes to memory
guard_a = MemoryGuard(policy=Policy.strict(), current_task="task_a")
guard_a.write("shared_config", "Task A's configuration")

# Task B tries to overwrite Task A's key
guard_b = MemoryGuard(policy=Policy.strict(), current_task="task_b")
guard_b.write("shared_config", "Overwritten by Task B")
# → Detected as cross-task contamination
```

## Multi-Tenant Isolation

For SaaS applications where multiple users share an agent:

```python
# Each user session gets its own task ID
guard = MemoryGuard(
    policy=Policy.strict(),
    current_task=f"user_{user_id}_session_{session_id}"
)
```

## Configuration

The detector is automatically enabled when `current_task` is provided to the MemoryGuard constructor. Without a task identifier, cross-task detection is skipped.
