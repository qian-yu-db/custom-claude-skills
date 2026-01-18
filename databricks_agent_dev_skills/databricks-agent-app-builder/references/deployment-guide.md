# Deployment Guide

Complete guide for deploying agents to Databricks Apps.

## Prerequisites

- Databricks CLI installed and configured
- Databricks workspace with Apps enabled
- uv Python package manager
- OAuth authentication (PATs not supported for Apps)

## Local Development

### First-Time Setup

```bash
# Run quickstart script
./scripts/quickstart.sh

# This will:
# 1. Install uv, nvm, Databricks CLI (if needed)
# 2. Configure Databricks authentication
# 3. Create MLflow experiment
# 4. Generate .env.local
```

### Manual Setup

```bash
# 1. Install dependencies
uv sync

# 2. Configure authentication
databricks auth login

# 3. Create .env.local
cp .env.example .env.local

# 4. Create MLflow experiment
DATABRICKS_USERNAME=$(databricks current-user me | jq -r .userName)
EXPERIMENT_RESPONSE=$(databricks experiments create-experiment /Users/$DATABRICKS_USERNAME/my-agent)
EXPERIMENT_ID=$(echo $EXPERIMENT_RESPONSE | jq -r .experiment_id)

# 5. Update .env.local with experiment ID
sed -i '' "s/MLFLOW_EXPERIMENT_ID=.*/MLFLOW_EXPERIMENT_ID=$EXPERIMENT_ID/" .env.local
```

### Run Locally

```bash
# Start server (default port 8000)
uv run start-server

# With hot-reload
uv run start-server --reload

# Custom port
uv run start-server --port 8001
```

### Test Locally

```bash
# Conversational agent
curl -X POST http://localhost:8000/invocations \
  -H "Content-Type: application/json" \
  -d '{"input": [{"role": "user", "content": "hello"}]}'

# Non-conversational agent
curl -X POST http://localhost:8000/invocations \
  -H "Content-Type: application/json" \
  -d '{"document_text": "...", "questions": ["..."]}'
```

## Deploy to Databricks Apps

### Option 1: Using deploy.sh Script

```bash
# Create and deploy new app
./scripts/deploy.sh my-agent-app --create

# Update existing app
./scripts/deploy.sh my-agent-app --update

# Dry run (show commands)
./scripts/deploy.sh my-agent-app --dry-run
```

### Option 2: Manual Deployment

```bash
# 1. Create app
databricks apps create my-agent-app

# 2. Get username
DATABRICKS_USERNAME=$(databricks current-user me | jq -r .userName)

# 3. Sync files to workspace
databricks sync . "/Users/$DATABRICKS_USERNAME/my-agent-app"

# 4. Deploy
databricks apps deploy my-agent-app \
  --source-code-path /Workspace/Users/$DATABRICKS_USERNAME/my-agent-app
```

### View Deployment Status

```bash
# Get app info
databricks apps get my-agent-app

# List all apps
databricks apps list
```

## Query Deployed App

### Get OAuth Token

```bash
# Generate OAuth token (required - PATs not supported)
databricks auth token
```

### Make Request

```bash
# Replace <app-url> with your app's URL
curl -X POST <app-url>/invocations \
  -H "Authorization: Bearer <oauth-token>" \
  -H "Content-Type: application/json" \
  -d '{"input": [{"role": "user", "content": "hello"}]}'
```

### Streaming Request

```bash
curl -X POST <app-url>/invocations \
  -H "Authorization: Bearer <oauth-token>" \
  -H "Content-Type: application/json" \
  -d '{"input": [{"role": "user", "content": "hello"}], "stream": true}'
```

## app.yaml Configuration

### Backend Only

```yaml
command: ["uv", "run", "start-server"]

env:
  - name: MLFLOW_TRACKING_URI
    value: "databricks"
  - name: MLFLOW_REGISTRY_URI
    value: "databricks-uc"
  - name: MLFLOW_EXPERIMENT_ID
    valueFrom: experiment
```

### With Frontend

```yaml
command: ["uv", "run", "start-app"]

env:
  - name: MLFLOW_TRACKING_URI
    value: "databricks"
  - name: MLFLOW_REGISTRY_URI
    value: "databricks-uc"
  - name: API_PROXY
    value: "http://localhost:8000/invocations"
  - name: CHAT_APP_PORT
    value: "3000"
  - name: CHAT_PROXY_TIMEOUT_SECONDS
    value: "600"
  - name: MLFLOW_EXPERIMENT_ID
    valueFrom: experiment
```

## Environment Variables

### Required

| Variable | Description |
|----------|-------------|
| `MLFLOW_EXPERIMENT_ID` | MLflow experiment for tracing |
| `MLFLOW_TRACKING_URI` | Set to "databricks" |
| `MLFLOW_REGISTRY_URI` | Set to "databricks-uc" |

### Authentication (Local)

| Variable | Description |
|----------|-------------|
| `DATABRICKS_CONFIG_PROFILE` | Profile name (e.g., "DEFAULT") |
| `DATABRICKS_HOST` | Workspace URL (alternative) |
| `DATABRICKS_TOKEN` | PAT token (alternative) |

### Frontend (Optional)

| Variable | Description |
|----------|-------------|
| `API_PROXY` | Backend URL for frontend |
| `CHAT_APP_PORT` | Frontend port (default: 3000) |
| `CHAT_PROXY_TIMEOUT_SECONDS` | Request timeout |

## Troubleshooting

### Authentication Errors

```bash
# Re-authenticate
databricks auth login

# Verify authentication
databricks current-user me
```

### Deployment Failures

```bash
# Check app logs
databricks apps get my-agent-app

# View detailed status
databricks apps describe my-agent-app
```

### Missing Experiment

```bash
# Create new experiment
databricks experiments create-experiment /Users/$DATABRICKS_USERNAME/my-agent

# List experiments
databricks experiments list
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Deploy Agent App

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Databricks CLI
        run: curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh

      - name: Configure Databricks
        env:
          DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}
          DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_TOKEN }}
        run: |
          databricks configure --token

      - name: Deploy
        run: |
          DATABRICKS_USERNAME=$(databricks current-user me | jq -r .userName)
          databricks sync . "/Users/$DATABRICKS_USERNAME/my-agent-app"
          databricks apps deploy my-agent-app \
            --source-code-path /Workspace/Users/$DATABRICKS_USERNAME/my-agent-app
```

## Security Considerations

1. **OAuth Only**: Databricks Apps require OAuth tokens, not PATs
2. **Environment Variables**: Never commit `.env.local` to version control
3. **Secrets**: Use Databricks secrets for sensitive values
4. **Network**: Apps run within Databricks network boundary

## Monitoring

### MLflow Tracing

All requests are automatically traced to MLflow:
- View traces in MLflow Experiment UI
- Track latency, errors, and model usage
- Debug with full request/response logs

### App Metrics

```bash
# View app metrics
databricks apps metrics my-agent-app
```
