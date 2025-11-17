# Quick Reference: Databricks Agent Deploy to Model Serving via DAB

## Common Commands

### DAB Commands

```bash
# Validate bundle
databricks bundle validate -t <target>

# Deploy bundle
databricks bundle deploy -t <target> --var="databricks_profile=<profile>"

# Destroy bundle resources
databricks bundle destroy -t <target>

# Run bundle job (for evaluation)
databricks bundle run -t <target> <job-name>
```

### Model Serving Commands

```bash
# List endpoints
databricks serving-endpoints list

# Get endpoint details
databricks serving-endpoints get --name <endpoint-name>

# Query endpoint
databricks serving-endpoints query-endpoint \
    --name <endpoint-name> \
    --json '{"messages": [{"role": "user", "content": "query"}]}'

# Update endpoint config
databricks serving-endpoints update-config \
    --name <endpoint-name> \
    --json-file config.json

# Delete endpoint
databricks serving-endpoints delete --name <endpoint-name>
```

### MLflow Commands

```bash
# List experiments
mlflow experiments search

# List runs in experiment
mlflow runs list --experiment-id <exp-id>

# Get run details
mlflow runs describe --run-id <run-id>

# List registered models
mlflow models list

# Get model version
mlflow models get-version --name <model-name> --version <version>
```

## DAB File Structure

### databricks.yml

```yaml
bundle:
  name: agent-deployment

include:
  - resources/*.yml

variables:
  catalog: main
  schema: agents
  model_name: my_agent
  endpoint_name: my-agent-endpoint

targets:
  dev:
    mode: development
    workspace:
      profile: ${var.databricks_profile}
  prod:
    mode: production
    workspace:
      profile: ${var.databricks_profile}
```

### resources/model_serving.yml

```yaml
resources:
  model_serving_endpoints:
    ${var.endpoint_name}:
      config:
        served_entities:
          - entity_name: ${var.catalog}.${var.schema}.${var.model_name}
            entity_version: "1"
            workload_size: Small
            scale_to_zero_enabled: true
```

## Deployment Workflow

### 1. Log Agent to MLflow

```python
import mlflow

mlflow.set_experiment("/Users/{user}/agent-experiments/my-agent")

with mlflow.start_run():
    logged_model = mlflow.langchain.log_model(
        lc_model="agent.py",
        artifact_path="agent",
        pip_requirements=["mlflow", "langchain", "langgraph"]
    )
```

### 2. Register Model

```python
registered_model = mlflow.register_model(
    model_uri=logged_model.model_uri,
    name="main.agents.my_agent"
)
```

### 3. Create DAB Structure

```bash
mkdir -p agent-dab/{resources,src/agent,scripts}
# Create databricks.yml and resource files
```

### 4. Deploy

```bash
cd agent-dab
databricks bundle deploy -t dev --var="databricks_profile=my-profile"
```

## Agent Framework Examples

### LangGraph

```python
# Log LangGraph agent
mlflow.langchain.log_model(
    lc_model="path/to/agent.py",
    artifact_path="agent",
    pip_requirements=[
        "langchain",
        "langgraph",
        "databricks-langchain"
    ]
)
```

### OpenAI SDK

```python
# Log OpenAI agent as pyfunc
class OpenAIAgent(mlflow.pyfunc.PythonModel):
    def predict(self, context, model_input):
        # Agent logic
        pass

mlflow.pyfunc.log_model(
    artifact_path="agent",
    python_model=OpenAIAgent(),
    pip_requirements=["openai"]
)
```

### Custom Agent

```python
# Log custom agent as pyfunc
class CustomAgent(mlflow.pyfunc.PythonModel):
    def predict(self, context, model_input):
        # Agent logic
        pass

mlflow.pyfunc.log_model(
    artifact_path="agent",
    python_model=CustomAgent(),
    pip_requirements=[...]
)
```

## Environment Configuration

### Workload Sizes

- **Small**: 1-2 vCPUs, 4-8 GB RAM (dev/testing)
- **Medium**: 4-8 vCPUs, 16-32 GB RAM (production)
- **Large**: 8-16 vCPUs, 32-64 GB RAM (high traffic)

### Environment Variables

```yaml
environment_vars:
  DATABRICKS_HOST: ${workspace.host}
  DATABRICKS_TOKEN: {{secrets/scope/key}}
  CUSTOM_VAR: value
```

### Traffic Routing

```yaml
traffic_config:
  routes:
    - served_model_name: model-v1
      traffic_percentage: 90
    - served_model_name: model-v2
      traffic_percentage: 10
```

## Deployment Targets

### Development

```yaml
targets:
  dev:
    mode: development
    variables:
      catalog: dev
      endpoint_name: my-agent-dev
```

### Production

```yaml
targets:
  prod:
    mode: production
    variables:
      catalog: prod
      endpoint_name: my-agent-prod
    permissions:
      - level: CAN_MANAGE
        group_name: ml-engineers
```

## Testing

### Local Test

```bash
# Test agent locally before deployment
python -c "from src.agent.agent import agent; print(agent.invoke({'messages': [...]}))"
```

### Endpoint Test

```bash
# Test deployed endpoint
curl -X POST https://<workspace-url>/serving-endpoints/<endpoint-name>/invocations \
  -H "Authorization: Bearer <token>" \
  -d '{"messages": [{"role": "user", "content": "test"}]}'
```

## Troubleshooting

### Validation Errors

```bash
# Check bundle syntax
databricks bundle validate -t dev

# View deployment plan
databricks bundle plan -t dev
```

### Endpoint Issues

```bash
# Check endpoint status
databricks serving-endpoints get --name <endpoint-name>

# View endpoint logs
databricks serving-endpoints logs --name <endpoint-name>
```

### Model Issues

```bash
# Verify model exists
mlflow models get --name <model-name>

# Check model version
mlflow models get-version --name <model-name> --version <version>
```

## Common Variables

```yaml
variables:
  # Unity Catalog
  catalog: main
  schema: agents
  model_name: my_agent

  # Endpoint
  endpoint_name: my-agent-endpoint
  workload_size: Small

  # Deployment
  databricks_profile: my-profile
  model_version: "1"

  # Auto-capture
  enable_auto_capture: true
```

## Permissions

### Endpoint Permissions

```yaml
permissions:
  - level: CAN_QUERY      # Query endpoint
    user_name: user@company.com
  - level: CAN_MANAGE     # Manage endpoint
    group_name: ml-engineers
```

### Model Permissions

```bash
# Grant model permissions via CLI
databricks models set-permissions \
    --name <model-name> \
    --json '{"access_control_list": [...]}'
```

## Update Strategies

### In-place Update

```bash
# Update model version
databricks bundle deploy -t prod --var="model_version=2"
```

### Blue/Green Deployment

```yaml
traffic_config:
  routes:
    - served_model_name: model-blue
      traffic_percentage: 0
    - served_model_name: model-green
      traffic_percentage: 100
```

### Canary Deployment

```yaml
traffic_config:
  routes:
    - served_model_name: model-v1
      traffic_percentage: 95
    - served_model_name: model-v2
      traffic_percentage: 5
```

## Monitoring

### Auto-capture

```yaml
auto_capture_config:
  catalog_name: ${var.catalog}
  schema_name: ${var.schema}
  table_name_prefix: ${var.endpoint_name}
  enabled: true
```

### Query Captured Data

```sql
SELECT * FROM main.agents.my_agent_endpoint_payload
WHERE timestamp > current_timestamp() - INTERVAL 1 DAY
LIMIT 100
```

## CI/CD Integration

### GitHub Actions

```yaml
- name: Deploy Agent
  run: |
    databricks bundle validate -t ${{ env.TARGET }}
    databricks bundle deploy -t ${{ env.TARGET }}
```

### Azure DevOps

```yaml
- script: |
    databricks bundle validate -t $(TARGET)
    databricks bundle deploy -t $(TARGET)
  displayName: 'Deploy Agent DAB'
```
