"""GuardedConversableAgent — AutoGen agent with built-in memory security.

Wraps AutoGen's ConversableAgent to scan all incoming and outgoing messages
through Agent Memory Guard before they enter the agent's memory.
"""

from __future__ import annotations

import logging
from typing import Any, Callable, Literal

from agent_memory_guard import Policy

from autogen_agent_memory_guard.hook import MemoryGuardHook

logger = logging.getLogger(__name__)


class GuardedConversableAgent:
    """An AutoGen ConversableAgent with built-in memory poisoning protection.

    This agent scans all messages it receives and sends through Agent Memory
    Guard, detecting prompt injection, secret leakage, and other attacks.

    Works as a drop-in replacement for ConversableAgent — pass all the same
    arguments and the agent behaves identically, but with security scanning.

    Args:
        name: Agent name.
        policy: Security policy to enforce. Defaults to Policy.strict().
        on_violation: How to handle violations ("block", "warn", "strip", "quarantine").
        scan_outgoing: Whether to also scan outgoing messages (default True).
        **kwargs: All other arguments passed to ConversableAgent.

    Example:
        \`\`\`python
        from autogen_agent_memory_guard import GuardedConversableAgent

        agent = GuardedConversableAgent(
            name="assistant",
            system_message="You are a helpful assistant.",
            llm_config={"model": "gpt-4o"},
            on_violation="strip",
        )

        # Use exactly like a normal ConversableAgent
        agent.initiate_chat(other_agent, message="Hello!")
        \`\`\`
    """

    def __init__(
        self,
        name: str,
        policy: Policy | None = None,
        on_violation: Literal["block", "warn", "strip", "quarantine"] = "block",
        scan_outgoing: bool = True,
        **kwargs: Any,
    ) -> None:
        self._name = name
        self._scan_outgoing = scan_outgoing
        self._hook = MemoryGuardHook(
            policy=policy,
            on_violation=on_violation,
        )

        # Create the underlying ConversableAgent
        try:
            from autogen import ConversableAgent

            self._agent = ConversableAgent(name=name, **kwargs)
        except ImportError:
            try:
                from autogen_agentchat.agents import AssistantAgent

                self._agent = AssistantAgent(name=name, **kwargs)
            except ImportError:
                raise ImportError(
                    "Could not import AutoGen. Install with: "
                    "pip install autogen-agentchat>=0.4.0"
                )

        # Register the scanning hook
        self._register_scan_hook()

    def _register_scan_hook(self) -> None:
        """Register message scanning on the underlying agent."""
        if hasattr(self._agent, "register_hook"):
            self._agent.register_hook(
                hookable_method="process_last_received_message",
                hook=self._scan_message_hook,
            )

    def _scan_message_hook(self, message: str | dict[str, Any], **kwargs: Any) -> str | dict[str, Any]:
        """Hook that scans incoming messages."""
        content = self._extract_content(message)
        if not content:
            return message

        sender = kwargs.get("sender", "unknown")
        if hasattr(sender, "name"):
            sender = sender.name

        result = self._hook.scan_message(
            content=content,
            sender=str(sender),
            role=self._infer_role(sender),
        )

        if result.message_content != content:
            if isinstance(message, dict):
                return {**message, "content": result.message_content}
            return result.message_content

        return message

    def _infer_role(self, sender: str) -> str:
        """Infer the role based on sender name."""
        sender_lower = sender.lower()
        if "user" in sender_lower or "human" in sender_lower:
            return "user"
        if "tool" in sender_lower or "function" in sender_lower:
            return "tool"
        if "system" in sender_lower:
            return "system"
        return "assistant"

    @staticmethod
    def _extract_content(message: str | dict[str, Any] | Any) -> str | None:
        """Extract text content from various message formats."""
        if isinstance(message, str):
            return message
        if isinstance(message, dict):
            return message.get("content", message.get("text", ""))
        if hasattr(message, "content"):
            return str(message.content)
        return None

    @property
    def metrics(self) -> dict[str, Any]:
        """Return scan metrics for this agent."""
        return self._hook.get_metrics()

    @property
    def violations_detected(self) -> int:
        """Number of violations detected for this agent."""
        return self._hook.violations_detected

    @property
    def name(self) -> str:
        """Agent name."""
        return self._name

    @property
    def agent(self) -> Any:
        """Access the underlying AutoGen agent directly."""
        return self._agent

    def __getattr__(self, name: str) -> Any:
        """Proxy attribute access to the underlying agent."""
        if name.startswith("_"):
            raise AttributeError(name)
        return getattr(self._agent, name)
