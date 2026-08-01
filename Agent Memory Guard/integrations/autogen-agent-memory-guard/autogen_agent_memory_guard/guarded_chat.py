"""GuardedGroupChat — drop-in replacement for AutoGen GroupChat with memory security.

Scans every message before it enters the group chat history, preventing
memory poisoning attacks in multi-agent conversations.
"""

from __future__ import annotations

import logging
from typing import Any, Literal, Sequence

from agent_memory_guard import Policy

from autogen_agent_memory_guard.hook import MemoryGuardHook

logger = logging.getLogger(__name__)


class GuardedGroupChat:
    """A security-hardened wrapper around AutoGen group chat conversations.

    Intercepts all messages flowing through the group chat and scans them
    for prompt injection, secret leakage, and other memory poisoning attacks
    before they enter the shared conversation history.

    This is the recommended integration point for multi-agent AutoGen setups.

    Args:
        agents: List of AutoGen agents participating in the chat.
        policy: Security policy to enforce. Defaults to Policy.strict().
        on_violation: How to handle violations ("block", "warn", "strip", "quarantine").
        max_round: Maximum number of conversation rounds.
        admin_name: Name of the admin agent (if any).
        **kwargs: Additional arguments passed to the underlying GroupChat.

    Example:
        ```python
        from autogen_agent_memory_guard import GuardedGroupChat
        from autogen import ConversableAgent, GroupChatManager

        agent1 = ConversableAgent("researcher", llm_config=config)
        agent2 = ConversableAgent("writer", llm_config=config)

        # All messages are scanned before entering history
        chat = GuardedGroupChat(
            agents=[agent1, agent2],
            on_violation="strip",  # Remove malicious content silently
        )

        manager = GroupChatManager(groupchat=chat.group_chat)
        agent1.initiate_chat(manager, message="Research AI security trends")
        ```
    """

    def __init__(
        self,
        agents: Sequence[Any],
        policy: Policy | None = None,
        on_violation: Literal["block", "warn", "strip", "quarantine"] = "block",
        max_round: int = 20,
        admin_name: str = "Admin",
        **kwargs: Any,
    ) -> None:
        self._hook = MemoryGuardHook(
            policy=policy,
            on_violation=on_violation,
        )
        self._agents = list(agents)
        self._max_round = max_round
        self._admin_name = admin_name
        self._kwargs = kwargs
        self._group_chat: Any = None

        # Register hooks on all agents
        self._register_hooks()

    def _register_hooks(self) -> None:
        """Register message scanning hooks on all agents."""
        for agent in self._agents:
            if hasattr(agent, "register_hook"):
                agent.register_hook(
                    hookable_method="process_last_received_message",
                    hook=self._scan_incoming_message,
                )
            elif hasattr(agent, "_process_received_message"):
                original_process = agent._process_received_message

                def make_guarded_process(orig, ag):
                    def guarded_process(message, sender, *args, **kw):
                        content = self._extract_content(message)
                        if content:
                            result = self._hook.scan_message(
                                content=content,
                                sender=getattr(sender, "name", str(sender)),
                                role="assistant",
                            )
                            if not result.allowed:
                                return None
                            if result.message_content != content:
                                if isinstance(message, dict):
                                    message["content"] = result.message_content
                                elif isinstance(message, str):
                                    message = result.message_content
                        return orig(message, sender, *args, **kw)
                    return guarded_process

                agent._process_received_message = make_guarded_process(
                    original_process, agent
                )

    def _scan_incoming_message(
        self, message: str | dict[str, Any], **kwargs: Any
    ) -> str | dict[str, Any]:
        """Hook function that scans messages before processing."""
        content = self._extract_content(message)
        if not content:
            return message

        sender = kwargs.get("sender", "unknown")
        if hasattr(sender, "name"):
            sender = sender.name

        result = self._hook.scan_message(
            content=content,
            sender=str(sender),
            role="assistant",
        )

        if result.message_content != content:
            if isinstance(message, dict):
                message = {**message, "content": result.message_content}
            else:
                message = result.message_content

        return message

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
    def group_chat(self) -> Any:
        """Lazily create and return the underlying AutoGen GroupChat."""
        if self._group_chat is None:
            try:
                from autogen import GroupChat

                self._group_chat = GroupChat(
                    agents=self._agents,
                    messages=[],
                    max_round=self._max_round,
                    admin_name=self._admin_name,
                    **self._kwargs,
                )
            except ImportError:
                try:
                    from autogen_agentchat.teams import RoundRobinGroupChat

                    self._group_chat = RoundRobinGroupChat(
                        participants=self._agents,
                        max_turns=self._max_round,
                    )
                except ImportError:
                    raise ImportError(
                        "Could not import AutoGen. Install with: "
                        "pip install autogen-agentchat>=0.4.0"
                    )
        return self._group_chat

    @property
    def metrics(self) -> dict[str, Any]:
        """Return scan metrics for this group chat."""
        return self._hook.get_metrics()

    @property
    def violations_detected(self) -> int:
        """Number of violations detected in this chat."""
        return self._hook.violations_detected
