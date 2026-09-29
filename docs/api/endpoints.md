# API Endpoints

## POST /scan

Scan a text value for security threats without persisting to memory.

**Request:**

```json
{
  "text": "string (required) — the text to analyze",
  "key": "string (optional) — memory key context",
  "source": "string (optional) — source identifier"
}
```

**Response (200):**

```json
{
  "action": "allow | quarantine | block",
  "threats_detected": 2,
  "events": [
    {
      "detector": "PromptInjectionDetector",
      "severity": "critical",
      "action": "quarantine",
      "message": "Prompt injection pattern detected"
    }
  ]
}
```

---

## POST /write

Write a key-value pair to the guarded memory store. The value is screened by all detectors before storage.

**Request:**

```json
{
  "key": "string (required)",
  "value": "string (required)",
  "source": "string (optional)"
}
```

**Response (200):**

```json
{
  "action": "allow | quarantine | block",
  "key": "user_preference",
  "stored": true,
  "events": []
}
```

**Response (403) — blocked by policy:**

```json
{
  "detail": "Write blocked by policy: Prompt injection detected"
}
```

---

## POST /read

Read a value from the guarded memory store.

**Request:**

```json
{
  "key": "string (required)"
}
```

**Response (200):**

```json
{
  "key": "user_preference",
  "value": "dark mode",
  "exists": true
}
```

---

## GET /events

Retrieve recent security events from the guard.

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | int | 100 | Max events to return |
| `severity` | string | all | Filter by severity |

**Response (200):**

```json
{
  "events": [
    {
      "timestamp": "2025-01-15T10:30:00Z",
      "detector": "PromptInjectionDetector",
      "severity": "critical",
      "action": "quarantine",
      "key": "system_prompt",
      "message": "Prompt injection pattern detected"
    }
  ],
  "total": 1
}
```

---

## GET /health

Health check endpoint for load balancers and monitoring.

**Response (200):**

```json
{
  "status": "healthy",
  "version": "0.3.0",
  "uptime_seconds": 3600,
  "policy": "strict",
  "detectors_active": 10
}
```

---

## GET /stats

Guard statistics and metrics.

**Response (200):**

```json
{
  "total_writes": 1500,
  "total_reads": 3200,
  "threats_detected": 45,
  "threats_blocked": 42,
  "quarantined_keys": 12,
  "detectors": {
    "PromptInjectionDetector": {"triggers": 20},
    "SensitiveDataDetector": {"triggers": 15},
    "ToolAbuseDetector": {"triggers": 10}
  }
}
```

---

## POST /scan/file

Scan a Python file's content for memory security vulnerabilities.

**Request:**

```json
{
  "content": "string (required) — file content",
  "filename": "string (optional) — filename for context"
}
```

**Response (200):**

```json
{
  "filename": "agent.py",
  "findings": [
    {
      "line": 42,
      "severity": "critical",
      "detector": "PromptInjectionDetector",
      "message": "Prompt injection pattern in string literal",
      "snippet": "memory.write('sys', 'ignore all previous...')"
    }
  ],
  "total_findings": 1
}
```

## Error Responses

All endpoints return standard HTTP error codes:

| Code | Meaning |
|------|---------|
| 400 | Invalid request body |
| 403 | Write blocked by policy |
| 404 | Key not found (for reads) |
| 500 | Internal server error |
