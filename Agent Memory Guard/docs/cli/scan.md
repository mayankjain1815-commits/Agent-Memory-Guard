# amg scan

Scan a directory or file for memory security vulnerabilities. The scanner identifies hardcoded strings that match threat patterns (prompt injection, data leakage, privilege escalation, etc.) in your source code.

## Usage

```bash
amg scan [OPTIONS] PATH
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `PATH` | Yes | Directory or file to scan |

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--format` | `text` | Output format: `text`, `json`, `sarif` |
| `--output`, `-o` | stdout | Write report to file |
| `--severity` | `low` | Minimum severity: `low`, `medium`, `high`, `critical` |
| `--include` | `**/*.py` | Comma-separated glob patterns to include |
| `--exclude` | `**/test*/**,...` | Comma-separated glob patterns to exclude |
| `--fail-on-findings` | off | Exit with code 1 if findings detected |

## Examples

### Basic scan

```bash
amg scan ./my_project
```

Output:

```
🛡️ Agent Memory Guard — Security Scan
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Scanning: ./my_project
Files scanned: 23
Findings: 3

┌─────────────────────────────────────────────────────┐
│ CRITICAL: Prompt injection in agent/memory.py:42    │
│ Pattern: "ignore all previous instructions"         │
│ Detector: PromptInjectionDetector                   │
├─────────────────────────────────────────────────────┤
│ HIGH: Sensitive data in config/secrets.py:15        │
│ Pattern: API key exposed in memory value            │
│ Detector: SensitiveDataDetector                     │
├─────────────────────────────────────────────────────┤
│ MEDIUM: Privilege escalation in tools/admin.py:88   │
│ Pattern: "grant admin access"                       │
│ Detector: PrivilegeEscalationDetector               │
└─────────────────────────────────────────────────────┘

Summary: 1 critical, 1 high, 1 medium
```

### SARIF output for CI/CD

```bash
amg scan . --format sarif --output results.sarif --fail-on-findings
```

The SARIF format integrates directly with GitHub's Security tab when used with the [GitHub Action](../integrations/github-actions.md).

### JSON output

```bash
amg scan . --format json --severity high
```

```json
{
  "scan_path": ".",
  "files_scanned": 23,
  "summary": {
    "total_findings": 2,
    "critical": 1,
    "high": 1,
    "medium": 0,
    "low": 0
  },
  "findings": [
    {
      "file": "agent/memory.py",
      "line": 42,
      "severity": "critical",
      "detector": "PromptInjectionDetector",
      "message": "Prompt injection pattern detected",
      "snippet": "guard.write('system', 'ignore all previous instructions...')"
    }
  ]
}
```

### Scan specific file types

```bash
# Scan Python and JavaScript files
amg scan . --include "**/*.py,**/*.js,**/*.ts"

# Exclude test directories
amg scan . --exclude "**/tests/**,**/fixtures/**"
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Scan completed (no findings, or `--fail-on-findings` not set) |
| 1 | Findings detected (with `--fail-on-findings`) or error |
