# Databricks Asset Bundle Structure for Agent Deployment

## Overview

This document describes the complete structure of a Databricks Asset Bundle (DAB) for deploying AI agents to Model Serving.

## Complete Directory Structure

```
agent-dab/
├── databricks.yml                      # Main bundle configuration
├── resources/                          # Resource definitions
│   ├── model_serving.yml              # Model serving endpoint
│   ├── evaluation_job.yml             # Optional: Evaluation job
│   └── experiments.yml                # Optional: MLflow experiments
├── src/                                # Source code
│   ├── agent/                         # Agent implementation
│   │   ├── __init__.py
│   │   ├── agent.py                   # Main agent code
│   │   ├── config.py                  # Configuration
│   │   ├── tools.py                   # Agent tools (optional)
│   │   └── prompts.py                 # Prompts (optional)
│   ├── evaluation/                    # Evaluation code (optional)
│   │   ├── __init__.py
│   │   ├── eval.py                    # Evaluation script
│   │   └── metrics.py                 # Custom metrics
│   └── utils/                         # Utility functions
│       ├── __init__.py
│       └── helpers.py
├── tests/                              # Tests (optional)
│   ├── __init__.py
│   ├── test_agent.py
│   └── test_integration.py
├── scripts/                            # Deployment scripts
│   ├── deploy.sh                      # Main deployment script
│   ├── log_and_register.py           # MLflow logging
│   ├── update_endpoint.sh            # Update endpoint
│   └── test_endpoint.sh              # Test deployed endpoint
├── config/                             # Configuration files
│   ├── dev.yml                        # Dev environment config
│   ├── staging.yml                    # Staging environment config
│   └── prod.yml                       # Prod environment config
├── requirements.txt                    # Python dependencies
├── .gitignore                         # Git ignore patterns
└── README.md                          # Documentation
```

## databricks.yml

The main bundle configuration file.

### Basic Structure

```yaml
bundle:
  name: <bundle-name>

# Include additional resource files
include:
  - resources/*.yml

# Define variables
variables:
  catalog:
    description: Unity Catalog name
    default: main
  schema:
    description: Schema name
    default: agents
  model_name:
    description: Model name
    default: my_agent
  endpoint_name:
    description: Serving endpoint name
    default: my-agent-endpoint
  databricks_profile:
    description: Databricks CLI profile
    default: DEFAULT

# Define deployment targets
targets:
  dev:
    mode: development
    default: true
    workspace:
      host: ${DATABRICKS_HOST}
      profile: ${var.databricks_profile}
    variables:
      catalog: dev
      schema: agents
      endpoint_name: ${bundle.name}-dev

  staging:
    mode: development
    workspace:
      host: ${DATABRICKS_HOST}
      profile: ${var.databricks_profile}
    variables:
      catalog: staging
      schema: agents
      endpoint_name: ${bundle.name}-staging

  prod:
    mode: production
    workspace:
      host: ${DATABRICKS_HOST}
      profile: ${var.databricks_profile}
    variables:
      catalog: prod
      schema: agents
      endpoint_name: ${bundle.name}-prod
```

### Advanced Features

```yaml
# Git integration
bundle:
  name: my-agent
  git:
    branch: main
    origin_url: https://github.com/org/repo

# Deployment permissions
targets:
  prod:
    permissions:
      - level: CAN_MANAGE
        group_name: ml-engineers
      - level: CAN_VIEW
        group_name: ml-users

# Run-as configuration (service principal)
targets:
  prod:
    run_as:
      service_principal_name: sp-agent-deployment
```

## resources/model_serving.yml

Model serving endpoint configuration.

### Basic Configuration

```yaml
resources:
  model_serving_endpoints:
    ${var.endpoint_name}:
      config:
        served_entities:
          - entity_name: ${var.catalog}.${var.schema}.${var.model_name}
            entity_version: "${var.model_version}"
            workload_size: ${var.workload_size}
            scale_to_zero_enabled: true

            # Environment variables
            environment_vars:
              DATABRICKS_HOST: ${workspace.host}
              DATABRICKS_TOKEN: "{{secrets/${var.secret_scope}/${var.secret_key}}}"
```

### Advanced Configuration

```yaml
resources:
  model_serving_endpoints:
    ${var.endpoint_name}:
      config:
        # Multiple model versions with traffic routing
        served_entities:
          - name: ${var.model_name}-v1
            entity_name: ${var.catalog}.${var.schema}.${var.model_name}
            entity_version: "1"
            workload_size: Small
            scale_to_zero_enabled: true

          - name: ${var.model_name}-v2
            entity_name: ${var.catalog}.${var.schema}.${var.model_name}
            entity_version: "2"
            workload_size: Small
            scale_to_zero_enabled: true

        # Traffic routing between versions
        traffic_config:
          routes:
            - served_model_name: ${var.model_name}-v1
              traffic_percentage: 90
            - served_model_name: ${var.model_name}-v2
              traffic_percentage: 10

        # Auto-capture for monitoring
        auto_capture_config:
          catalog_name: ${var.catalog}
          schema_name: ${var.schema}
          table_name_prefix: ${var.endpoint_name}
          enabled: true

      # Endpoint permissions
      permissions:
        - level: CAN_QUERY
          group_name: ml-users
        - level: CAN_MANAGE
          group_name: ml-engineers
        - level: CAN_MANAGE
          user_name: admin@company.com
```

### Workload Size Options

- **Small**: 1-2 vCPUs, 4-8 GB RAM
- **Medium**: 4-8 vCPUs, 16-32 GB RAM
- **Large**: 8-16 vCPUs, 32-64 GB RAM

## resources/evaluation_job.yml

Optional evaluation job configuration.

```yaml
resources:
  jobs:
    ${var.endpoint_name}_evaluation:
      name: ${var.endpoint_name}-evaluation
      description: Evaluate agent performance

      tasks:
        - task_key: run_evaluation
          notebook_task:
            notebook_path: ./src/evaluation/eval.py
            base_parameters:
              endpoint_name: ${var.endpoint_name}
              model_name: ${var.catalog}.${var.schema}.${var.model_name}
              evaluation_dataset: ${var.catalog}.${var.schema}.eval_dataset

          new_cluster:
            node_type_id: ${var.node_type}
            spark_version: ${var.spark_version}
            num_workers: 0  # Single node
            spark_conf:
              spark.databricks.cluster.profile: singleNode

          libraries:
            - pypi:
                package: mlflow>=2.10.0
            - pypi:
                package: databricks-agents>=0.1.0

      # Schedule (optional)
      schedule:
        quartz_cron_expression: "0 0 * * * ?"  # Daily at midnight
        timezone_id: "UTC"
        pause_status: UNPAUSED

      # Email notifications
      email_notifications:
        on_start:
          - ml-team@company.com
        on_success:
          - ml-team@company.com
        on_failure:
          - ml-team@company.com
        no_alert_for_skipped_runs: false

      # Job permissions
      permissions:
        - level: CAN_MANAGE
          group_name: ml-engineers
        - level: CAN_VIEW
          group_name: ml-users
```

## resources/experiments.yml

Optional MLflow experiments configuration.

```yaml
resources:
  experiments:
    ${var.endpoint_name}_experiment:
      name: /Users/${workspace.current_user.userName}/experiments/${var.endpoint_name}
      description: MLflow experiment for ${var.endpoint_name}

      permissions:
        - level: CAN_MANAGE
          group_name: ml-engineers
        - level: CAN_READ
          group_name: ml-users
```

## Variable Interpolation

DAB supports various variable types:

### Bundle Variables

```yaml
${bundle.name}           # Bundle name
${bundle.environment}    # Deployment environment
${bundle.target}         # Target name (dev, prod, etc.)
```

### Target Variables

```yaml
${var.catalog}           # User-defined variable
${var.model_name}        # User-defined variable
```

### Workspace Variables

```yaml
${workspace.host}                              # Workspace URL
${workspace.current_user.userName}            # Current user
${workspace.current_user.id}                  # Current user ID
```

### Environment Variables

```yaml
${DATABRICKS_HOST}       # From environment
${DATABRICKS_TOKEN}      # From environment
```

### Secrets

```yaml
{{secrets/scope/key}}    # Databricks secret
```

## Configuration Files

### config/dev.yml

```yaml
# Development-specific configuration
catalog: dev
schema: agents
workload_size: Small
scale_to_zero_enabled: true
model_version: latest
auto_capture_enabled: false
```

### config/prod.yml

```yaml
# Production-specific configuration
catalog: prod
schema: agents
workload_size: Medium
scale_to_zero_enabled: false
model_version: "1"  # Pin to specific version
auto_capture_enabled: true
```

## Best Practices

### 1. Use Variables for Environment-Specific Values

```yaml
variables:
  catalog: main
  schema: agents

targets:
  dev:
    variables:
      catalog: dev
  prod:
    variables:
      catalog: prod
```

### 2. Separate Resource Definitions

Keep resource definitions in separate files:
- `resources/model_serving.yml`
- `resources/evaluation_job.yml`
- `resources/experiments.yml`

### 3. Use Secrets for Sensitive Data

Never hardcode credentials:

```yaml
# Bad
environment_vars:
  API_KEY: "abc123"

# Good
environment_vars:
  API_KEY: "{{secrets/my-scope/api-key}}"
```

### 4. Pin Production Versions

```yaml
targets:
  dev:
    variables:
      model_version: latest
  prod:
    variables:
      model_version: "1"  # Specific version
```

### 5. Set Appropriate Permissions

```yaml
targets:
  prod:
    permissions:
      - level: CAN_MANAGE
        group_name: ml-engineers
```

## Deployment Modes

### Development Mode

- Allows recreation of resources
- Faster iteration
- Less strict validation

```yaml
targets:
  dev:
    mode: development
```

### Production Mode

- Prevents accidental deletion
- Requires explicit approval for changes
- Stricter validation

```yaml
targets:
  prod:
    mode: production
```

## Advanced Features

### Git Integration

```yaml
bundle:
  name: my-agent
  git:
    branch: main
    origin_url: https://github.com/org/repo
    commit: ${GIT_COMMIT}
```

### Service Principal Authentication

```yaml
targets:
  prod:
    run_as:
      service_principal_name: sp-agent-deployment
```

### Conditional Resources

```yaml
resources:
  jobs:
    ${var.endpoint_name}_evaluation:
      # Only create in prod
      condition: ${bundle.target == "prod"}
```

## Validation and Deployment

### Validate Bundle

```bash
databricks bundle validate -t dev
```

### Deploy Bundle

```bash
databricks bundle deploy -t dev --var="databricks_profile=my-profile"
```

### View Deployment Plan

```bash
databricks bundle plan -t dev
```

### Destroy Resources

```bash
databricks bundle destroy -t dev
```
