"""Exceptions for the AutoGen Agent Memory Guard integration."""

from __future__ import annotations

from typing import Any


class MemoryGuardViolation(Exception):
    """Raised when a message violates the memory guard policy.

    Attributes:
        message_content: The original message that triggered the violation.
        violation_type: Category of violation (e.g., "prompt_injection").
        sender: Name of the agent that sent the violating message.
        details: Additional context about the violation.
    """

    def __init__(
        self,
        message_content: str,
        violation_type: str,
        sender: str = "unknown",
        details: dict[str, Any] | None = None,
    ) -> None:
        self.message_content = message_content
        self.violation_type = violation_type
        self.sender = sender
        self.details = details or {}

        super().__init__(
            f"Memory guard violation [{violation_type}] from '{sender}': "
            f"{message_content[:100]}{'...' if len(message_content) > 100 else ''}"
        )
