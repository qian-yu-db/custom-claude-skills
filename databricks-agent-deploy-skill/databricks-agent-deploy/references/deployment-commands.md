# Databricks Apps Deployment Commands

## Prerequisites

- Databricks CLI installed and configured
- Databricks workspace with Apps enabled
- Unity Catalog enabled workspace
- Proper permissions (workspace admin or app creator)

## CLI Installation

```bash
# Install Databricks CLI
pip install databricks-cli

# Configure authentication
databricks configure --token
# Enter workspace URL: https://<workspace>.cloud.databricks.com
# Enter token: <your-personal-access-token>
```

## App Creation

### Create App via CLI

```bash
# Basic app creation
databricks apps create my-agent-app

# With JSON configuration
databricks apps create --json '{
  "name": "my-agent-chatbot",
  "description": "AI agent deployed on Databricks Apps",
  "resources": [
    {
      "name": "serving-endpoint",
      "serving_endpoint": {
        "name": "my-model-endpoint",
        "permission": "CAN_QUERY"
      }
    }
  ]
}'
```

### Create App with Resources

```bash
# Save configuration to file
cat > app_config.json << 'EOF'
{
  "name": "my-agent-app",
  "description": "Production agent application",
  "resources": [
    {
      "name": "model-endpoint",
      "serving_endpoint": {
        "name": "agent-model-serving",
        "permission": "CAN_QUERY"
      }
    },
    {
      "name": "vector-search",
      "serving_endpoint": {
        "name": "vector-search-endpoint",
        "permission": "CAN_QUERY"
      }
    }
  ]
}
EOF

# Create app from config
databricks apps create --json "$(cat app_config.json)"
```

## Source Code Deployment

### Upload and Deploy

```bash
# Get current username
DATABRICKS_USERNAME=$(databricks current-user me | jq -r .userName)

# Sync local code to workspace
databricks sync /path/to/local/agent "/Users/$DATABRICKS_USERNAME/my-agent-app"

# Deploy the app
databricks apps deploy my-agent-app \
  --source-code-path "/Workspace/Users/$DATABRICKS_USERNAME/my-agent-app"
```

### Deploy with Environment Variables

```bash
# Deploy with env vars
databricks apps deploy my-agent-app \
  --source-code-path "/Workspace/Users/$DATABRICKS_USERNAME/my-agent-app" \
  --env MODEL_ENDPOINT=my-model-endpoint \
  --env LOG_LEVEL=INFO
```

## App Management

### List Apps

```bash
# List all apps
databricks apps list

# Get specific app details
databricks apps get my-agent-app
```

### Update App

```bash
# Update app configuration
databricks apps update my-agent-app --json '{
  "description": "Updated agent application"
}'

# Redeploy with new code
databricks sync /path/to/updated/code "/Users/$DATABRICKS_USERNAME/my-agent-app"
databricks apps deploy my-agent-app \
  --source-code-path "/Workspace/Users/$DATABRICKS_USERNAME/my-agent-app"
```

### Delete App

```bash
# Delete app
databricks apps delete my-agent-app
```

## Permission Management

### Set Permissions via CLI

```bash
# Grant user access
databricks apps permissions update my-agent-app \
  --json '{
    "access_control_list": [
      {
        "user_name": "user@company.com",
        "permission_level": "CAN_VIEW"
      }
    ]
  }'

# Grant group access
databricks apps permissions update my-agent-app \
  --json '{
    "access_control_list": [
      {
        "group_name": "data-science-team",
        "permission_level": "CAN_MANAGE"
      }
    ]
  }'
```

### Permission Levels

- `CAN_VIEW`: Can view and use the app
- `CAN_RUN`: Can view and run the app
- `CAN_MANAGE`: Can view, run, and manage the app
- `IS_OWNER`: Full control over the app

## MLflow Model Logging

### Log Agent as MLflow Model

```python
import mlflow

# Log agent with git-based versioning
with mlflow.start_run():
    # Log model
    mlflow.pyfunc.log_model(
        artifact_path="agent",
        python_model=agent,
        registered_model_name="my-agent-model",
        pip_requirements=[
            "mlflow",
            "langchain",
            "databricks-sdk"
        ],
        code_paths=["agent.py", "utils.py"]
    )
    
    # Log git commit hash
    import subprocess
    git_commit = subprocess.check_output(
        ["git", "rev-parse", "HEAD"]
    ).decode().strip()
    mlflow.log_param("git_commit", git_commit)
```

### Register Model from Run

```bash
# Get run ID
RUN_ID="<your-run-id>"

# Register model
databricks models create \
  --name my-agent-model \
  --run-id $RUN_ID \
  --model-path agent
```

## Monitoring and Logs

### View App Logs

```bash
# View recent logs
databricks apps logs my-agent-app

# Follow logs in real-time
databricks apps logs my-agent-app --follow

# Get logs from specific time
databricks apps logs my-agent-app --since 1h
```

### Access App URL

```bash
# Get app URL
databricks apps get my-agent-app | jq -r .url

# Open in browser (macOS)
open $(databricks apps get my-agent-app | jq -r .url)
```

## Testing Deployment

### Test Invoke Endpoint

```bash
# Test non-streaming invoke
curl -X POST "https://<workspace>.cloud.databricks.com/apps/my-agent-app/invocations" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ],
    "stream": false
  }'
```

### Test Streaming Endpoint

```bash
# Test streaming invoke
curl -X POST "https://<workspace>.cloud.databricks.com/apps/my-agent-app/invocations" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Tell me a story"}
    ],
    "stream": true
  }'
```

## Complete Deployment Script

```bash
#!/bin/bash
set -e

# Configuration
APP_NAME="my-agent-app"
LOCAL_PATH="./agent-app"
ENDPOINT_NAME="agent-model-endpoint"

# Get username
USERNAME=$(databricks current-user me | jq -r .userName)
WORKSPACE_PATH="/Users/$USERNAME/$APP_NAME"

echo "🚀 Deploying $APP_NAME to Databricks Apps"

# Create app if it doesn't exist
if ! databricks apps get $APP_NAME &> /dev/null; then
  echo "📦 Creating new app: $APP_NAME"
  databricks apps create --json "{
    \"name\": \"$APP_NAME\",
    \"resources\": [{
      \"name\": \"serving-endpoint\",
      \"serving_endpoint\": {
        \"name\": \"$ENDPOINT_NAME\",
        \"permission\": \"CAN_QUERY\"
      }
    }]
  }"
fi

# Sync source code
echo "📤 Syncing source code to workspace"
databricks sync $LOCAL_PATH $WORKSPACE_PATH

# Deploy app
echo "🔄 Deploying app"
databricks apps deploy $APP_NAME \
  --source-code-path "/Workspace$WORKSPACE_PATH"

# Get app URL
APP_URL=$(databricks apps get $APP_NAME | jq -r .url)
echo "✅ Deployment complete!"
echo "🌐 App URL: $APP_URL"

# Test health endpoint
echo "🏥 Testing health endpoint"
curl -s "$APP_URL/health" | jq

echo "✨ Done!"
```
