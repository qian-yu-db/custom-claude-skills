# Databricks Agent Deployment Workflow

## Overview

This document describes the complete workflow for deploying AI agents on Databricks Apps instead of Model Serving endpoints.

## Key Benefits of Apps vs Model Serving

- **Faster authentication validation**: Test authentication with tools, endpoints, and Genie spaces in seconds
- **Git-based versioning**: Use MLflow git-based logged models for version control
- **Real-time tracing**: Built-in MLflow tracing for debugging and monitoring
- **Local development**: Use AI coding tools like Claude Code or Cursor to develop agents locally
- **Custom server behavior**: Full control over async server to handle agent invocation exactly as desired

## Core Components

### 1. Agent Implementation
The agent code that defines your AI agent's behavior, including:
- Tool definitions and integrations
- Prompt templates and system instructions
- Model configuration (LLM selection, parameters)
- Response formatting logic

### 2. Async Server
A FastAPI-based server that:
- Routes requests from `/invocations` to your agent
- Handles streaming and non-streaming responses
- Manages authentication and authorization
- Provides health check endpoints

### 3. MLflow Integration
- Automatic tracing of all agent interactions
- Model logging with git-based versioning
- Signature inference for input/output schemas
- Model registry integration for deployment

### 4. Databricks Apps Deployment
- App creation and configuration
- Resource provisioning (compute, endpoints)
- Permission management
- URL generation for access

## Development Workflow

### Phase 1: Local Development
1. Clone or create agent template
2. Implement agent logic with tools
3. Test locally with MLflow tracing
4. Validate authentication with external services

### Phase 2: MLflow Logging
1. Log agent as MLflow model
2. Include git commit hash for versioning
3. Verify signature compatibility
4. Test model loading and inference

### Phase 3: App Deployment
1. Create Databricks App via CLI or API
2. Configure compute resources
3. Deploy app with source code
4. Set permissions for users/groups

### Phase 4: Testing & Monitoring
1. Test app endpoints (stream and invoke)
2. Monitor MLflow traces
3. Review error logs and metrics
4. Iterate on agent implementation

## Agent Templates

Templates typically include:
- **Agent code**: Main agent implementation with decorators
- **Requirements**: Python dependencies (mlflow, langchain, etc.)
- **Config files**: App configuration and environment variables
- **Server code**: Async server setup with routing
- **Tests**: Unit and integration tests

## Authentication Patterns

### Tool Authentication
- Use Databricks secrets for API keys
- Configure Unity Catalog external connections
- Pass credentials securely to tools

### Endpoint Authentication
- Personal access tokens (development)
- OAuth 2.0 (production recommended)
- Service principal credentials

### Genie Space Authentication
- Genie API authentication
- Space-level permissions
- Query execution credentials

## Streaming vs Invoke

### Stream Method
- Real-time token streaming
- Better UX for long responses
- Requires client-side handling
- Use decorator: `@agent.stream_method`

### Invoke Method
- Complete response returned at once
- Simpler client implementation
- Easier error handling
- Use decorator: `@agent.invoke_method`

## Best Practices

1. **Always use git-based MLflow logging** for version control
2. **Test authentication locally** before deploying to Apps
3. **Use decorators** for stream and invoke methods
4. **Enable MLflow tracing** for all agent interactions
5. **Configure proper permissions** on Apps and resources
6. **Use OAuth** instead of PATs for production
7. **Monitor traces** regularly for quality and performance
8. **Implement health checks** in your async server
9. **Handle errors gracefully** with proper status codes
10. **Document tool usage** in agent prompts
