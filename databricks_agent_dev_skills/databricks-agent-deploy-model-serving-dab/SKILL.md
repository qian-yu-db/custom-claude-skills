---
name: databricks-agent-deploy-model-serving-dab
description: Deploy AI agents (LangGraph, OpenAI SDK, or custom frameworks) to Databricks Model Serving using Databricks Asset Bundles (DAB). Use when deploying agents to Model Serving with infrastructure-as-code, multi-environment management (dev/staging/prod), serverless compute, and optional evaluation jobs.
---

# Databricks Agent Deploy to Model Serving via DAB

Deploy AI agents to Databricks Model Serving using Databricks Asset Bundles (DAB) for infrastructure-as-code deployment with environment management, MLflow integration, and optional evaluation.

## Key Concepts

### Deployment Flow
1. **Log agent** to MLflow with dependencies
2. **Register model** in Unity Catalog
3. **Create DAB configuration** with model serving endpoint
4. **Deploy using DAB** with specified profile
5. **Optional: Run evaluation** using DAB jobs

### Supported Frameworks
- **LangGraph**: Full LangGraph applications with state management
- **OpenAI SDK**: Agents using OpenAI Assistants API
- **Custom**: Any agent following MLflow pyfunc pattern

See [references/agent_frameworks.md](references/agent_frameworks.md) for complete implementation examples of all frameworks.

## Step-by-Step Workflow

### Step 1: Analyze Agent Code

Determine: framework type, dependencies, environment variables/secrets, model endpoints, vector search indexes, and tools used.

### Step 2: Log Agent to MLflow

Use `scripts/log_and_register.py` or log manually:

```bash
python scripts/log_and_register.py \
    --agent-path src/agent/agent.py \
    --model-name main.agents.my_agent \
    --agent-type langgraph
```

### Step 3: Register Model

```python
model_name = "main.agents.my_agent"  # catalog.schema.model_name
registered_model = mlflow.register_model(model_uri=model_uri, name=model_name)
```

### Step 4: Create DAB Structure

```
agent-dab/
├── databricks.yml              # Main DAB configuration
├── resources/
│   ├── model_serving.yml       # Model serving endpoint config
│   └── evaluation_job.yml      # Optional: Evaluation job
├── src/agent/                  # Agent implementation
├── scripts/
│   ├── deploy.sh               # Deployment script
│   └── log_and_register.py     # MLflow logging script
└── requirements.txt
```

### Step 5: Generate databricks.yml

```yaml
bundle:
  name: my-agent-deployment

include:
  - resources/*.yml

variables:
  catalog:
    description: Unity Catalog name
    default: main
  schema:
    default: agents
  model_name:
    default: my_agent
  endpoint_name:
    default: my-agent-endpoint

targets:
  dev:
    mode: development
    default: true
    workspace:
      host: ${DATABRICKS_HOST}
    variables:
      catalog: dev
      endpoint_name: my-agent-dev
  prod:
    mode: production
    workspace:
      host: ${DATABRICKS_HOST}
    variables:
      catalog: prod
      endpoint_name: my-agent-prod
    permissions:
      - level: CAN_MANAGE
        group_name: ml-engineers
```

### Step 6: Generate Model Serving Configuration

Create `resources/model_serving.yml`:

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
            environment_vars:
              DATABRICKS_HOST: ${workspace.host}
        auto_capture_config:
          catalog_name: ${var.catalog}
          schema_name: ${var.schema}
          table_name_prefix: ${var.endpoint_name}
          enabled: true
      permissions:
        - level: CAN_QUERY
          group_name: ml-users
        - level: CAN_MANAGE
          group_name: ml-engineers
```

### Step 7: Deploy

```bash
# Using the deployment script
./scripts/deploy.sh dev my-databricks-profile

# Or directly
databricks bundle validate -t dev
databricks bundle deploy -t dev
databricks serving-endpoints query-endpoint \
    --name my-agent-dev \
    --json '{"messages": [{"role": "user", "content": "Hello"}]}'
```

See [references/deployment_commands.md](references/deployment_commands.md) for complete CLI reference.

## Best Practices

1. **Version control** all DAB configurations
2. **Separate environments** using different catalogs/schemas for dev/staging/prod
3. **Secrets management**: Use Databricks Secrets for API keys
4. **Model versions**: Pin versions in production, use "latest" in dev
5. **Auto-capture**: Enable for monitoring and debugging
6. **Testing**: Test in dev before promoting to prod

## Common Issues

| Issue | Solution |
|-------|----------|
| Bundle validation fails | Check databricks.yml syntax and required fields |
| Endpoint creation fails | Verify model exists in Unity Catalog with proper permissions |
| Agent returns errors | Check environment variables and dependencies in serving config |
| Deployment hangs | Check Databricks CLI connection and profile configuration |

## References

- [references/agent_frameworks.md](references/agent_frameworks.md) - Framework-specific examples (LangGraph, OpenAI, custom RAG)
- [references/dab_structure.md](references/dab_structure.md) - Detailed DAB file structure
- [references/deployment_commands.md](references/deployment_commands.md) - CLI command reference
- [scripts/deploy.sh](scripts/deploy.sh) - Deployment script
- [scripts/log_and_register.py](scripts/log_and_register.py) - MLflow logging script
