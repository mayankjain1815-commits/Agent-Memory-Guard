# OWASP Agent Memory Guard — MCP Server

An [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) server that exposes Agent Memory Guard's scanning capabilities to any MCP-compatible AI agent.

## Quick Start

```bash
# Install
pip install amg-mcp-server

# Run
amg-mcp-server
```

## Tools Provided

| Tool | Description |
|------|-------------|
| `scan_memory_entry` | Scan a single memory entry for threats |
| `scan_memory_batch` | Scan multiple entries in one call |
| `validate_before_store` | Gate check before writing to memory |
| `validate_before_recall` | Gate check before injecting recalled memory |
| `get_threat_categories` | List all detectable threat types |

## Configuration (Claude Desktop)

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "agent-memory-guard": {
      "command": "amg-mcp-server"
    }
  }
}
```

## Threat Categories Detected

- **Prompt Injection** — system token injection, chat-ML delimiters
- **Secret Leakage** — API keys, tokens, private keys
- **Role Hijacking** — identity manipulation attempts
- **Instruction Override** — "ignore previous instructions" patterns
- **Data Exfiltration** — outbound data transfer attempts
- **Integrity Tampering** — fact manipulation in stored memories

## Links

- [OWASP Project Page](https://owasp.org/www-project-agent-memory-guard/)
- [PyPI Package](https://pypi.org/project/agent-memory-guard/)
- [MCP Protocol Spec](https://modelcontextprotocol.io/)
