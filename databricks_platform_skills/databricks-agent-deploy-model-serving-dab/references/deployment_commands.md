# Deployment Commands Reference

## Overview

Complete reference for deploying agents using Databricks Asset Bundles and managing Model Serving endpoints.

## Databricks CLI Installation

### Install/Upgrade CLI

```bash
# Install
pip install databricks-cli

# Upgrade to latest
pip install --upgrade databricks-cli
```

### Configure Profile

```bash
# Interactive configuration
databricks configure --profile my-profile

# Manual configuration
cat > ~/.databrickscfg << EOF
[my-profile]
host = https://your-workspace.cloud.databricks.com
token = dapi...
EOF
```

## DAB Commands

### Initialize Bundle

```bash
# Create new bundle from template
databricks bundle init

# Create bundle in specific directory
databricks bundle init my-agent-dab
```

### Validate Bundle

```bash
# Validate for default target (dev)
databricks bundle validate

# Validate for specific target
databricks bundle validate -t prod

# Validate with variables
databricks bundle validate -t dev --var="databricks_profile=my-profile"

# Verbose output
databricks bundle validate -t dev --debug
```

### Deploy Bundle

```bash
# Deploy to default target
databricks bundle deploy

# Deploy to specific target
databricks bundle deploy -t prod

# Deploy with profile
databricks bundle deploy -t prod --var="databricks_profile=my-profile"

# Force re-deployment
databricks bundle deploy -t dev --force

# Auto-approve (no confirmation)
databricks bundle deploy -t dev --auto-approve
```

### View Deployment Plan

```bash
# Show what will be deployed
databricks bundle plan -t dev

# Show detailed plan
databricks bundle plan -t dev --debug
```

### Destroy Bundle

```bash
# Destroy resources
databricks bundle destroy -t dev

# Auto-approve deletion
databricks bundle destroy -t dev --auto-approve

# Destroy specific target
databricks bundle destroy -t staging
```

### Run Bundle Job

```bash
# Run evaluation job
databricks bundle run -t dev my-agent-evaluation

# Run with parameters
databricks bundle run -t dev my-agent-evaluation \
    --param endpoint_name=my-agent-dev
```

## Model Serving Endpoint Commands

### List Endpoints

```bash
# List all endpoints
databricks serving-endpoints list

# List with details (JSON)
databricks serving-endpoints list --output json

# Filter by name pattern
databricks serving-endpoints list | grep my-agent
```

### Get Endpoint Details

```bash
# Get endpoint configuration
databricks serving-endpoints get --name my-agent-dev

# Get as JSON
databricks serving-endpoints get --name my-agent-dev --output json

# Get specific fields
databricks serving-endpoints get --name my-agent-dev | jq '.state'
```

### Query Endpoint

```bash
# Query with JSON input
databricks serving-endpoints query-endpoint \
    --name my-agent-dev \
    --json '{"messages": [{"role": "user", "content": "Hello"}]}'

# Query from file
databricks serving-endpoints query-endpoint \
    --name my-agent-dev \
    --json-file input.json

# Save response
databricks serving-endpoints query-endpoint \
    --name my-agent-dev \
    --json '{"messages": [...]}' \
    > response.json
```

### Update Endpoint

```bash
# Update endpoint configuration
databricks serving-endpoints update-config \
    --name my-agent-dev \
    --json-file new-config.json

# Update specific fields
databricks serving-endpoints update-config \
    --name my-agent-dev \
    --json '{
        "served_entities": [{
            "entity_name": "main.agents.my_agent",
            "entity_version": "2",
            "workload_size": "Small"
        }]
    }'
```

### Create Endpoint (Manual)

```bash
# Create endpoint from config file
databricks serving-endpoints create \
    --json-file endpoint-config.json

# Create endpoint inline
databricks serving-endpoints create \
    --json '{
        "name": "my-agent-manual",
        "config": {
            "served_entities": [...]
        }
    }'
```

### Delete Endpoint

```bash
# Delete endpoint
databricks serving-endpoints delete --name my-agent-dev

# Force delete (no confirmation)
databricks serving-endpoints delete --name my-agent-dev --no-wait
```

### Get Endpoint Logs

```bash
# Get recent logs
databricks serving-endpoints logs --name my-agent-dev

# Stream logs
databricks serving-endpoints logs --name my-agent-dev --follow

# Get logs from specific time range
databricks serving-endpoints logs \
    --name my-agent-dev \
    --start-time "2024-01-01T00:00:00Z" \
    --end-time "2024-01-01T23:59:59Z"
```

## MLflow Commands

### Experiments

```bash
# List experiments
mlflow experiments search

# Create experiment
mlflow experiments create --experiment-name /Users/me/my-experiment

# Get experiment by name
mlflow experiments get-by-name --name /Users/me/my-experiment

# Delete experiment
mlflow experiments delete --experiment-id 123
```

### Runs

```bash
# List runs in experiment
mlflow runs list --experiment-id 123

# Get run details
mlflow runs describe --run-id abc123

# Download artifacts
mlflow artifacts download \
    --run-id abc123 \
    --artifact-path agent \
    --dst-path ./downloaded-agent
```

### Models

```bash
# List registered models
mlflow models list

# Get model details
mlflow models get --name main.agents.my_agent

# Get specific version
mlflow models get-version \
    --name main.agents.my_agent \
    --version 1

# Delete model version
mlflow models delete-version \
    --name main.agents.my_agent \
    --version 1

# Transition model stage
mlflow models transition-stage \
    --name main.agents.my_agent \
    --version 2 \
    --stage Production
```

### Serve Model Locally (Testing)

```bash
# Serve model from Unity Catalog
mlflow models serve \
    --model-uri models:/main.agents.my_agent/1 \
    --port 5000

# Serve with environment variables
DATABRICKS_HOST=https://... \
DATABRICKS_TOKEN=dapi... \
mlflow models serve \
    --model-uri models:/main.agents.my_agent/1 \
    --port 5000

# Test local endpoint
curl -X POST http://localhost:5000/invocations \
    -H "Content-Type: application/json" \
    -d '{"messages": [{"role": "user", "content": "test"}]}'
```

## Unity Catalog Commands

### Catalogs

```bash
# List catalogs
databricks catalogs list

# Create catalog
databricks catalogs create --name my_catalog

# Get catalog details
databricks catalogs get --name my_catalog
```

### Schemas

```bash
# List schemas
databricks schemas list --catalog-name main

# Create schema
databricks schemas create \
    --catalog-name main \
    --name agents

# Get schema details
databricks schemas get \
    --catalog-name main \
    --name agents
```

### Models (UC)

```bash
# List models in schema
databricks registered-models list \
    --catalog-name main \
    --schema-name agents

# Get model details
databricks registered-models get \
    --full-name main.agents.my_agent

# Create model
databricks registered-models create \
    --catalog-name main \
    --schema-name agents \
    --name my_agent

# Delete model
databricks registered-models delete \
    --full-name main.agents.my_agent
```

## Secrets Management

### Create Secret Scope

```bash
# Create scope
databricks secrets create-scope --scope my-scope

# List scopes
databricks secrets list-scopes
```

### Manage Secrets

```bash
# Put secret (interactive)
databricks secrets put --scope my-scope --key api-key

# Put secret from file
databricks secrets put-secret \
    --scope my-scope \
    --key api-key \
    --string-value "abc123"

# List secrets
databricks secrets list --scope my-scope

# Delete secret
databricks secrets delete --scope my-scope --key api-key
```

### Use Secrets in DAB

```yaml
environment_vars:
  API_KEY: "{{secrets/my-scope/api-key}}"
  DATABASE_PASSWORD: "{{secrets/my-scope/db-password}}"
```

## Workspace File Commands

### Upload Files

```bash
# Upload single file
databricks workspace import \
    ./agent.py \
    /Workspace/Users/me/agent.py

# Upload directory
databricks workspace import-dir \
    ./src \
    /Workspace/Users/me/src

# Overwrite existing
databricks workspace import \
    ./agent.py \
    /Workspace/Users/me/agent.py \
    --overwrite
```

### Download Files

```bash
# Download file
databricks workspace export \
    /Workspace/Users/me/agent.py \
    ./agent.py

# Download directory
databricks workspace export-dir \
    /Workspace/Users/me/src \
    ./downloaded-src
```

## Complete Deployment Workflow

### 1. Prepare Environment

```bash
# Install dependencies
pip install databricks-cli mlflow

# Configure profile
databricks configure --profile my-profile

# Set environment variables
export DATABRICKS_HOST=https://...
export DATABRICKS_TOKEN=dapi...
```

### 2. Log and Register Agent

```python
# Run logging script
python scripts/log_and_register.py \
    --agent-path src/agent/agent.py \
    --model-name main.agents.my_agent \
    --agent-type langgraph
```

### 3. Validate Bundle

```bash
# Validate configuration
databricks bundle validate -t dev \
    --var="databricks_profile=my-profile"

# Check for errors
echo $?  # Should be 0
```

### 4. Deploy

```bash
# Deploy to development
databricks bundle deploy -t dev \
    --var="databricks_profile=my-profile"

# Check deployment status
databricks serving-endpoints get --name my-agent-dev
```

### 5. Test

```bash
# Query endpoint
databricks serving-endpoints query-endpoint \
    --name my-agent-dev \
    --json '{"messages": [{"role": "user", "content": "test"}]}'
```

### 6. Promote to Production

```bash
# Validate prod config
databricks bundle validate -t prod \
    --var="databricks_profile=my-profile"

# Deploy to prod
databricks bundle deploy -t prod \
    --var="databricks_profile=my-profile"
```

## Troubleshooting Commands

### Check CLI Version

```bash
databricks --version
mlflow --version
```

### Debug Mode

```bash
# Enable debug logging
databricks bundle deploy -t dev --debug

# Verbose mode
databricks serving-endpoints get --name my-agent-dev -v
```

### Test Authentication

```bash
# Test workspace connection
databricks workspace list /

# Test with specific profile
databricks workspace list / --profile my-profile
```

### View Endpoint State

```bash
# Check if endpoint is ready
databricks serving-endpoints get --name my-agent-dev | jq '.state.ready'

# Check config version
databricks serving-endpoints get --name my-agent-dev | jq '.state.config_update'
```

### Monitor Deployment

```bash
# Watch endpoint status
watch -n 5 'databricks serving-endpoints get --name my-agent-dev | jq .state'

# Check DAB deployment status
databricks bundle status -t dev
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Deploy Agent

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Install Databricks CLI
        run: pip install databricks-cli

      - name: Configure Databricks
        run: |
          echo "[DEFAULT]" > ~/.databrickscfg
          echo "host = ${{ secrets.DATABRICKS_HOST }}" >> ~/.databrickscfg
          echo "token = ${{ secrets.DATABRICKS_TOKEN }}" >> ~/.databrickscfg

      - name: Deploy Bundle
        run: |
          databricks bundle validate -t prod
          databricks bundle deploy -t prod
```

### Azure DevOps

```yaml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: UsePythonVersion@0
    inputs:
      versionSpec: '3.10'

  - script: |
      pip install databricks-cli
    displayName: 'Install Databricks CLI'

  - script: |
      databricks bundle validate -t $(TARGET)
      databricks bundle deploy -t $(TARGET)
    env:
      DATABRICKS_HOST: $(DATABRICKS_HOST)
      DATABRICKS_TOKEN: $(DATABRICKS_TOKEN)
    displayName: 'Deploy Agent'
```

## Environment-Specific Commands

### Development

```bash
# Quick iteration
databricks bundle deploy -t dev --auto-approve

# Test immediately
databricks serving-endpoints query-endpoint \
    --name my-agent-dev \
    --json '{"messages": [...]}'
```

### Staging

```bash
# Deploy to staging
databricks bundle deploy -t staging

# Run evaluation
databricks bundle run -t staging my-agent-evaluation
```

### Production

```bash
# Validate carefully
databricks bundle validate -t prod

# Review plan
databricks bundle plan -t prod

# Deploy with confirmation
databricks bundle deploy -t prod

# Verify deployment
databricks serving-endpoints get --name my-agent-prod | jq '.state'
```
