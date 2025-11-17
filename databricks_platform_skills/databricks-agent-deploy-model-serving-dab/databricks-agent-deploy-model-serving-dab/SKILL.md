# Databricks Agent Deploy to Model Serving via DAB

## Skill Overview

This skill enables deployment of AI agents (LangGraph, OpenAI SDK, or custom frameworks) to Databricks Model Serving using Databricks Asset Bundles (DAB). It provides a complete infrastructure-as-code approach for agent deployment with environment management, MLflow integration, and optional evaluation.

## When to Use This Skill

Use this skill when the user wants to:
- Deploy LangGraph agents to Databricks Model Serving using DAB
- Deploy OpenAI SDK agents to Databricks Model Serving using DAB
- Deploy custom agent frameworks to Model Serving using DAB
- Set up multi-environment agent deployments (dev/staging/prod)
- Use infrastructure-as-code for agent deployment
- Integrate agent deployment with CI/CD pipelines
- Manage agent deployments with version control

## Key Concepts

### Databricks Asset Bundles (DAB)
Infrastructure-as-code approach for Databricks resources, defined in `databricks.yml`:
- Model serving endpoints
- MLflow experiments
- Registered models
- Jobs (for evaluation)
- Permissions and access control

### Agent Deployment Flow
1. **Log agent** to MLflow with dependencies
2. **Register model** in Unity Catalog
3. **Create DAB configuration** with model serving endpoint
4. **Deploy using DAB** with specified profile
5. **Optional: Run evaluation** using DAB jobs

### Supported Agent Frameworks
- **LangGraph**: Full LangGraph applications with state management
- **OpenAI SDK**: Agents using OpenAI Assistants API
- **Custom frameworks**: Any agent following MLflow pyfunc pattern

## Step-by-Step Workflow

### Step 1: Analyze Agent Code

First, analyze the user's agent code to determine:
- Agent framework (LangGraph, OpenAI, custom)
- Required dependencies
- Environment variables/secrets needed
- Model endpoint names (if using Databricks LLMs)
- Vector search indexes (if using RAG)
- Tools/functions used

Example questions to ask:
- "What agent framework are you using? (LangGraph, OpenAI, custom)"
- "Which Databricks resources does your agent use? (LLM endpoints, vector search, etc.)"
- "What environment variables or secrets does your agent need?"
- "Which Databricks profile should be used for deployment?"

### Step 2: Create MLflow Logging Code

Generate code to log the agent to MLflow. This varies by framework:

#### For LangGraph Agents

```python
import mlflow
from databricks import agents

# Set experiment
mlflow.set_experiment("/Users/{user}/agent-experiments/my-langgraph-agent")

# Log the agent
with mlflow.start_run(run_name="langgraph-agent-v1"):
    logged_agent = mlflow.langchain.log_model(
        lc_model="path/to/agent.py",  # Path to agent code
        artifact_path="agent",
        input_example={
            "messages": [
                {"role": "user", "content": "What is Databricks?"}
            ]
        },
        pip_requirements=[
            "mlflow",
            "langchain",
            "langgraph",
            "databricks-langchain",
            "databricks-agents",
            # Add other dependencies
        ],
        # Optional: Include environment variables
        resources=[
            {
                "databricks_serving_endpoint": {
                    "name": "databricks-meta-llama-3-1-70b-instruct"
                }
            }
        ]
    )

    model_uri = logged_agent.model_uri
    print(f"Agent logged at: {model_uri}")
```

#### For OpenAI SDK Agents

```python
import mlflow
from openai import OpenAI

# Set experiment
mlflow.set_experiment("/Users/{user}/agent-experiments/my-openai-agent")

# Define pyfunc wrapper for OpenAI agent
class OpenAIAgentModel(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        import os
        from openai import OpenAI
        self.client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            base_url=os.environ.get("DATABRICKS_BASE_URL"),
        )
        self.assistant_id = context.model_config.get("assistant_id")

    def predict(self, context, model_input):
        # Implementation of agent logic
        messages = model_input["messages"]
        thread = self.client.beta.threads.create(messages=messages)
        run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant_id
        )
        # Poll and return response
        return {"messages": [...]}

# Log the agent
with mlflow.start_run(run_name="openai-agent-v1"):
    mlflow.pyfunc.log_model(
        artifact_path="agent",
        python_model=OpenAIAgentModel(),
        pip_requirements=[
            "mlflow",
            "openai",
            "databricks-agents",
        ],
        input_example={
            "messages": [
                {"role": "user", "content": "Help me with this task"}
            ]
        },
        model_config={
            "assistant_id": "asst_xxxxx"
        }
    )
```

#### For Custom Agents

```python
import mlflow

class CustomAgentModel(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        # Load your agent components
        pass

    def predict(self, context, model_input):
        # Implement agent logic
        pass

# Log the agent
with mlflow.start_run(run_name="custom-agent-v1"):
    mlflow.pyfunc.log_model(
        artifact_path="agent",
        python_model=CustomAgentModel(),
        pip_requirements=[
            "mlflow",
            # Add your dependencies
        ],
        input_example={"input": "sample query"}
    )
```

### Step 3: Register Model in Unity Catalog

After logging, register the model:

```python
from databricks import agents

# Register the model
model_name = "main.agents.my_agent"  # catalog.schema.model_name

registered_model = mlflow.register_model(
    model_uri=model_uri,
    name=model_name
)

model_version = registered_model.version
print(f"Registered model: {model_name} version {model_version}")
```

### Step 4: Create Databricks Asset Bundle Structure

Generate the DAB structure:

```
agent-dab/
├── databricks.yml              # Main DAB configuration
├── resources/
│   ├── model_serving.yml       # Model serving endpoint config
│   └── evaluation_job.yml      # Optional: Evaluation job
├── src/
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── agent.py            # Agent implementation
│   │   └── config.py           # Agent configuration
│   └── evaluation/
│       ├── __init__.py
│       └── eval.py             # Optional: Evaluation script
├── requirements.txt             # Python dependencies
└── README.md
```

### Step 5: Generate databricks.yml

Create the main DAB configuration:

```yaml
bundle:
  name: my-agent-deployment

# Include resource definitions
include:
  - resources/*.yml

# Variables for different environments
variables:
  catalog:
    description: Unity Catalog name
    default: main
  schema:
    description: Schema name
    default: agents
  model_name:
    description: Model name in Unity Catalog
    default: my_agent
  endpoint_name:
    description: Model serving endpoint name
    default: my-agent-endpoint

# Deployment targets
targets:
  dev:
    mode: development
    default: true
    workspace:
      host: ${DATABRICKS_HOST}
      profile: ${var.databricks_profile}
    variables:
      catalog: dev
      endpoint_name: my-agent-dev

  staging:
    mode: development
    workspace:
      host: ${DATABRICKS_HOST}
      profile: ${var.databricks_profile}
    variables:
      catalog: staging
      endpoint_name: my-agent-staging

  prod:
    mode: production
    workspace:
      host: ${DATABRICKS_HOST}
      profile: ${var.databricks_profile}
    variables:
      catalog: prod
      endpoint_name: my-agent-prod
    # Production requires approval
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
            entity_version: "1"  # Or use "latest" for always latest
            workload_size: Small  # Small, Medium, Large
            scale_to_zero_enabled: true

            # Environment variables for the agent
            environment_vars:
              DATABRICKS_HOST: ${workspace.host}
              # Add other environment variables

        # Traffic configuration for A/B testing
        traffic_config:
          routes:
            - served_model_name: ${var.catalog}.${var.schema}.${var.model_name}-1
              traffic_percentage: 100

        # Optional: Auto-capture configuration
        auto_capture_config:
          catalog_name: ${var.catalog}
          schema_name: ${var.schema}
          table_name_prefix: ${var.endpoint_name}
          enabled: true

      # Permissions
      permissions:
        - level: CAN_QUERY
          group_name: ml-users
        - level: CAN_MANAGE
          group_name: ml-engineers
```

### Step 7: Optional - Create Evaluation Job Configuration

Create `resources/evaluation_job.yml` (only if user requests evaluation):

```yaml
resources:
  jobs:
    ${var.endpoint_name}_evaluation:
      name: ${var.endpoint_name}-evaluation

      tasks:
        - task_key: evaluate_agent
          notebook_task:
            notebook_path: ./src/evaluation/eval.py
            base_parameters:
              endpoint_name: ${var.endpoint_name}
              model_name: ${var.catalog}.${var.schema}.${var.model_name}

          new_cluster:
            node_type_id: i3.xlarge
            spark_version: 14.3.x-scala2.12
            num_workers: 0  # Single node for evaluation
            spark_conf:
              spark.databricks.cluster.profile: singleNode

          libraries:
            - pypi:
                package: mlflow
            - pypi:
                package: databricks-agents

      schedule:
        quartz_cron_expression: "0 0 * * * ?"  # Daily at midnight
        timezone_id: "UTC"

      # Email notifications
      email_notifications:
        on_failure:
          - ml-team@company.com
```

### Step 8: Generate Deployment Scripts

Create `scripts/deploy.sh`:

```bash
#!/bin/bash

# Deploy agent using Databricks Asset Bundle
# Usage: ./scripts/deploy.sh [dev|staging|prod] [databricks-profile]

TARGET=${1:-dev}
PROFILE=${2:-DEFAULT}

echo "Deploying agent to $TARGET environment using profile $PROFILE"

# Validate the bundle
echo "Validating bundle..."
databricks bundle validate -t $TARGET --var="databricks_profile=$PROFILE"

if [ $? -ne 0 ]; then
    echo "Bundle validation failed. Please fix errors and try again."
    exit 1
fi

# Deploy the bundle
echo "Deploying bundle..."
databricks bundle deploy -t $TARGET --var="databricks_profile=$PROFILE"

if [ $? -eq 0 ]; then
    echo "Deployment successful!"
    echo "Endpoint: $(databricks bundle run -t $TARGET get_endpoint_url)"
else
    echo "Deployment failed."
    exit 1
fi
```

Create `scripts/log_and_register.py`:

```python
#!/usr/bin/env python3
"""
Log and register agent to MLflow and Unity Catalog
"""
import os
import sys
import mlflow
from pathlib import Path

def log_and_register_agent(
    agent_path: str,
    model_name: str,
    agent_type: str = "langgraph",
    pip_requirements: list = None,
    env_vars: dict = None
):
    """
    Log and register an agent to MLflow and Unity Catalog

    Args:
        agent_path: Path to agent code
        model_name: Unity Catalog model name (catalog.schema.model)
        agent_type: Type of agent (langgraph, openai, custom)
        pip_requirements: List of pip requirements
        env_vars: Dictionary of environment variables
    """
    # Set experiment
    experiment_name = f"/Users/{os.environ.get('USER')}/agent-experiments/{model_name.split('.')[-1]}"
    mlflow.set_experiment(experiment_name)

    # Default requirements
    if pip_requirements is None:
        pip_requirements = [
            "mlflow>=2.10.0",
            "databricks-agents>=0.1.0",
        ]

        if agent_type == "langgraph":
            pip_requirements.extend([
                "langchain",
                "langgraph",
                "databricks-langchain",
            ])
        elif agent_type == "openai":
            pip_requirements.extend([
                "openai",
            ])

    # Log the agent
    with mlflow.start_run(run_name=f"{model_name}-deployment"):
        if agent_type == "langgraph":
            logged_model = mlflow.langchain.log_model(
                lc_model=agent_path,
                artifact_path="agent",
                pip_requirements=pip_requirements,
                input_example={
                    "messages": [
                        {"role": "user", "content": "Hello"}
                    ]
                }
            )
        else:
            # For custom/openai, user needs to provide the model
            print(f"Please log your {agent_type} agent manually")
            sys.exit(1)

        model_uri = logged_model.model_uri
        print(f"Agent logged at: {model_uri}")

        # Register the model
        registered_model = mlflow.register_model(
            model_uri=model_uri,
            name=model_name
        )

        print(f"Model registered: {model_name} version {registered_model.version}")
        return registered_model.version

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Log and register agent")
    parser.add_argument("--agent-path", required=True, help="Path to agent code")
    parser.add_argument("--model-name", required=True, help="UC model name")
    parser.add_argument("--agent-type", default="langgraph",
                       choices=["langgraph", "openai", "custom"])

    args = parser.parse_args()

    log_and_register_agent(
        agent_path=args.agent_path,
        model_name=args.model_name,
        agent_type=args.agent_type
    )
```

### Step 9: Generate Deployment Instructions

Create a README.md for the DAB project:

```markdown
# Agent Deployment with Databricks Asset Bundle

## Prerequisites

1. Databricks CLI installed and configured
2. Agent code logged to MLflow
3. Model registered in Unity Catalog
4. Databricks profile configured

## Quick Start

### 1. Log and Register Agent

```bash
python scripts/log_and_register.py \
    --agent-path src/agent/agent.py \
    --model-name main.agents.my_agent \
    --agent-type langgraph
```

### 2. Deploy to Development

```bash
./scripts/deploy.sh dev my-databricks-profile
```

### 3. Deploy to Production

```bash
./scripts/deploy.sh prod my-databricks-profile
```

## Configuration

Edit `databricks.yml` to customize:
- Catalog/schema names
- Endpoint names
- Workload sizes
- Permissions

## Testing

Test the deployed endpoint:

```bash
databricks serving-endpoints query-endpoint \
    --name my-agent-dev \
    --json '{"messages": [{"role": "user", "content": "Hello"}]}'
```
```

### Step 10: Deploy the Agent

Guide the user through deployment:

```bash
# Step 1: Validate the bundle
databricks bundle validate -t dev --var="databricks_profile=my-profile"

# Step 2: Deploy the bundle
databricks bundle deploy -t dev --var="databricks_profile=my-profile"

# Step 3: Verify deployment
databricks serving-endpoints get --name my-agent-dev

# Step 4: Test the endpoint
databricks serving-endpoints query-endpoint \
    --name my-agent-dev \
    --json '{"messages": [{"role": "user", "content": "Test query"}]}'
```

## Helper Functions

### Generate Complete DAB Structure

```python
def generate_agent_dab_structure(
    agent_name: str,
    agent_type: str,
    model_name: str,
    databricks_profile: str,
    include_evaluation: bool = False,
    workload_size: str = "Small"
):
    """
    Generate complete DAB structure for agent deployment

    Returns: Dictionary with all file contents
    """
    files = {}

    # databricks.yml
    files["databricks.yml"] = generate_databricks_yml(
        agent_name, model_name
    )

    # resources/model_serving.yml
    files["resources/model_serving.yml"] = generate_model_serving_config(
        model_name, workload_size
    )

    # Optional: evaluation job
    if include_evaluation:
        files["resources/evaluation_job.yml"] = generate_evaluation_job(
            agent_name
        )

    # Deployment scripts
    files["scripts/deploy.sh"] = generate_deploy_script()
    files["scripts/log_and_register.py"] = generate_log_register_script()

    return files
```

### Update Model Serving Endpoint

```python
def update_model_serving_endpoint(
    endpoint_name: str,
    new_model_version: str,
    traffic_percentage: int = 100,
    dab_target: str = "dev"
):
    """
    Update model serving endpoint with new model version
    """
    # Update the model version in databricks.yml or pass as variable
    # Then redeploy
    import subprocess

    result = subprocess.run([
        "databricks", "bundle", "deploy",
        "-t", dab_target,
        "--var", f"model_version={new_model_version}"
    ])

    return result.returncode == 0
```

## Best Practices

1. **Version Control**: Always commit DAB configurations to git
2. **Separate Environments**: Use different catalogs/schemas for dev/staging/prod
3. **Secrets Management**: Use Databricks Secrets for API keys and credentials
4. **Model Versions**: Pin model versions in production, use "latest" in dev
5. **Auto-capture**: Enable auto-capture for monitoring and debugging
6. **Permissions**: Set appropriate permissions for each environment
7. **Testing**: Test in dev before promoting to prod
8. **Evaluation**: Only include evaluation jobs when explicitly requested

## Common Issues and Solutions

### Issue: Bundle validation fails
**Solution**: Check databricks.yml syntax and ensure all required fields are present

### Issue: Model serving endpoint creation fails
**Solution**: Verify model exists in Unity Catalog and user has permissions

### Issue: Agent returns errors when queried
**Solution**: Check environment variables and dependencies in model serving config

### Issue: Deployment hangs
**Solution**: Check Databricks CLI connection and profile configuration

## References

See reference documentation in `references/`:
- `dab_structure.md`: Detailed DAB file structure
- `model_serving_config.md`: Model serving configuration options
- `agent_frameworks.md`: Framework-specific examples
- `deployment_commands.md`: CLI command reference
