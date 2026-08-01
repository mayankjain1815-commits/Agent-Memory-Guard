"""AutoGen integration for OWASP Agent Memory Guard.

Provides drop-in memory security for AutoGen multi-agent conversations:
- GuardedGroupChat: Scans every message before it enters group chat history
- GuardedConversableAgent: Agent wrapper that guards memory reads/writes
- MemoryGuardHook: Low-level hook for custom AutoGen pipelines

Usage:
    from autogen_agent_memory_guard import GuardedGroupChat, GuardedConversableAgent

    # Protect an entire group chat
    chat = GuardedGroupChat(agents=[agent1, agent2])

    # Or protect individual agents
    agent = GuardedConversableAgent(
        name="assistant",
        llm_config=llm_config,
    )
"""

from autogen_agent_memory_guard.guarded_chat import GuardedGroupChat
from autogen_agent_memory_guard.guarded_agent import GuardedConversableAgent
from autogen_agent_memory_guard.hook import MemoryGuardHook
from autogen_agent_memory_guard.exceptions import MemoryGuardViolation

__all__ = [
    "GuardedGroupChat",
    "GuardedConversableAgent",
    "MemoryGuardHook",
    "MemoryGuardViolation",
]

__version__ = "0.1.0"
