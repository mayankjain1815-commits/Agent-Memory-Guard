# CrewAI Integration

Monitor and protect CrewAI agent memory operations with AMG's callback handler.

## Installation

```bash
pip install agent-memory-guard[crewai]
```

## Usage

```python
from crewai import Agent, Task, Crew
from agent_memory_guard import MemoryGuard, Policy
from agent_memory_guard.integrations.crewai import MemoryGuardCallback

# Create the AMG callback
guard = MemoryGuard(policy=Policy.strict())
amg_callback = MemoryGuardCallback(guard=guard)

# Create CrewAI agents with the callback
researcher = Agent(
    role="Researcher",
    goal="Find information about AI security",
    backstory="You are a security researcher...",
    callbacks=[amg_callback],
)

writer = Agent(
    role="Writer",
    goal="Write a report on findings",
    backstory="You are a technical writer...",
    callbacks=[amg_callback],
)

# Create tasks and crew as normal
task = Task(
    description="Research memory poisoning attacks",
    agent=researcher,
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[task],
)

# AMG monitors all memory operations during execution
result = crew.kickoff()
```

## How It Works

The `MemoryGuardCallback` hooks into CrewAI's lifecycle events:

- `on_task_start` — screens task descriptions before execution
- `on_task_complete` — screens task results before they enter memory
- `on_agent_action` — monitors agent actions for suspicious patterns

## Accessing Security Events

```python
# After crew execution
for event in guard.events:
    print(f"Agent: {event.source} | Threat: {event.message}")

# Check the callback's event log
for entry in amg_callback.event_log:
    print(f"Agent '{entry['agent']}' performed: {entry['action']}")
```

## Multi-Agent Protection

In multi-agent crews, AMG prevents one agent from poisoning another's memory:

```python
# If the researcher agent outputs malicious content,
# AMG blocks it before it reaches the writer agent's context
guard = MemoryGuard(
    policy=Policy.strict(),
    current_task="crew_research_task_1",
)
```
