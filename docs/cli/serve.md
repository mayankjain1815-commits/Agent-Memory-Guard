# amg serve

Start the Agent Memory Guard REST API server. This provides HTTP endpoints for scanning text, managing a guarded memory store, and retrieving security events — useful for polyglot environments or microservice architectures.

## Usage

```bash
amg serve [OPTIONS]
```

## Requirements

Requires the `server` extra:

```bash
pip install agent-memory-guard[server]
```

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--host` | `0.0.0.0` | Host to bind |
| `--port`, `-p` | `8000` | Port to listen on |
| `--reload` | off | Enable auto-reload (development) |
| `--policy` | `strict` | Default policy: `permissive`, `strict`, `tiered` |

## Examples

```bash
# Start with defaults
amg serve

# Custom port with tiered policy
amg serve --port 9000 --policy tiered

# Development mode with auto-reload
amg serve --reload --policy permissive
```

## API Documentation

Once running, interactive API docs are available at:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Docker Deployment

```dockerfile
FROM python:3.11-slim
RUN pip install agent-memory-guard[server]
EXPOSE 8000
HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1
CMD ["amg", "serve", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t amg-server .
docker run -p 8000:8000 amg-server
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `AMG_POLICY` | `strict` | Override the default policy |
| `AMG_LOG_LEVEL` | `info` | Set logging verbosity |

See [API Server documentation](../api/index.md) for full endpoint reference.
