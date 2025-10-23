#!/usr/bin/env python3
"""
Initialize a new Databricks agent project structure.

This script creates a complete agent project with all necessary files
for deployment on Databricks Apps.
"""

import os
import sys
from pathlib import Path


def create_agent_project(project_name: str, output_dir: str = "."):
    """Create a new agent project with complete structure"""
    
    project_path = Path(output_dir) / project_name
    
    if project_path.exists():
        print(f"❌ Error: Directory {project_path} already exists")
        sys.exit(1)
    
    print(f"🚀 Creating agent project: {project_name}")
    project_path.mkdir(parents=True)
    
    # Create directory structure
    dirs = [
        "src",
        "tests",
        "config"
    ]
    
    for dir_name in dirs:
        (project_path / dir_name).mkdir()
        print(f"✅ Created directory: {dir_name}/")
    
    # Create agent.py
    agent_code = '''"""
Main agent implementation
"""
import mlflow
from typing import Iterator, Dict, Any


class Agent:
    """AI Agent with MLflow tracing"""
    
    def __init__(self, model_name: str = "databricks-meta-llama-3-1-70b-instruct"):
        self.model_name = model_name
        # Initialize your client/tools here
        
    @mlflow.trace
    def invoke(self, messages: list[dict]) -> str:
        """
        Non-streaming invoke method
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            
        Returns:
            String response from agent
        """
        # TODO: Implement agent logic
        user_message = messages[-1]["content"]
        return f"Agent received: {user_message}"
    
    @mlflow.trace
    def stream(self, messages: list[dict]) -> Iterator[str]:
        """
        Streaming invoke method
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            
        Yields:
            String chunks from agent response
        """
        # TODO: Implement streaming logic
        response = self.invoke(messages)
        for char in response:
            yield char


# Create agent instance
agent = Agent()
'''
    
    (project_path / "src" / "agent.py").write_text(agent_code)
    print("✅ Created src/agent.py")
    
    # Create server.py
    server_code = '''"""
FastAPI server for agent deployment on Databricks Apps
"""
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
import uvicorn
from src.agent import agent

app = FastAPI(title="Databricks Agent API")


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "agent": "ready"}


@app.post("/invocations")
async def invoke(request: Request):
    """
    Main agent invocation endpoint
    
    Supports both streaming and non-streaming responses
    """
    try:
        data = await request.json()
        messages = data.get("messages", [])
        stream = data.get("stream", False)
        
        if not messages:
            return JSONResponse(
                status_code=400,
                content={"error": "messages field is required"}
            )
        
        if stream:
            return StreamingResponse(
                agent.stream(messages),
                media_type="text/event-stream"
            )
        else:
            result = agent.invoke(messages)
            return {"response": result}
            
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    
    (project_path / "server.py").write_text(server_code)
    print("✅ Created server.py")
    
    # Create requirements.txt
    requirements = '''mlflow>=2.9.0
databricks-sdk>=0.18.0
fastapi>=0.104.0
uvicorn>=0.24.0
langchain>=0.1.0
langchain-community>=0.0.20
pydantic>=2.5.0
'''
    
    (project_path / "requirements.txt").write_text(requirements)
    print("✅ Created requirements.txt")
    
    # Create app.yaml
    app_config = f'''name: {project_name}
description: AI agent deployed on Databricks Apps

# Python version
python: "3.11"

# Entry point for the server
command:
  - python
  - server.py

# Environment variables (optional)
env:
  LOG_LEVEL: INFO
  MODEL_ENDPOINT: databricks-meta-llama-3-1-70b-instruct
'''
    
    (project_path / "app.yaml").write_text(app_config)
    print("✅ Created app.yaml")
    
    # Create deploy.sh
    deploy_script = f'''#!/bin/bash
# Deployment script for {project_name}

set -e

APP_NAME="{project_name}"
LOCAL_PATH="."

echo "🚀 Deploying $APP_NAME to Databricks Apps"

# Get username
USERNAME=$(databricks current-user me | jq -r .userName)
WORKSPACE_PATH="/Users/$USERNAME/$APP_NAME"

# Create app if it doesn't exist
if ! databricks apps get $APP_NAME &> /dev/null; then
  echo "📦 Creating new app: $APP_NAME"
  databricks apps create $APP_NAME
fi

# Sync source code
echo "📤 Syncing source code to workspace"
databricks sync $LOCAL_PATH $WORKSPACE_PATH

# Deploy app
echo "🔄 Deploying app"
databricks apps deploy $APP_NAME \\
  --source-code-path "/Workspace$WORKSPACE_PATH"

# Get app URL
APP_URL=$(databricks apps get $APP_NAME | jq -r .url)
echo "✅ Deployment complete!"
echo "🌐 App URL: $APP_URL"

echo "✨ Done!"
'''
    
    (project_path / "deploy.sh").write_text(deploy_script)
    (project_path / "deploy.sh").chmod(0o755)
    print("✅ Created deploy.sh")
    
    # Create README.md
    readme = f'''# {project_name}

AI agent deployed on Databricks Apps.

## Project Structure

```
{project_name}/
├── src/
│   └── agent.py          # Agent implementation
├── tests/                # Unit tests
├── config/               # Configuration files
├── server.py             # FastAPI server
├── requirements.txt      # Python dependencies
├── app.yaml             # App configuration
├── deploy.sh            # Deployment script
└── README.md            # This file
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure Databricks CLI:
```bash
databricks configure --token
```

## Local Testing

Run the server locally:
```bash
python server.py
```

Test the endpoint:
```bash
curl -X POST http://localhost:8000/invocations \\
  -H "Content-Type: application/json" \\
  -d '{{"messages": [{{"role": "user", "content": "Hello!"}}], "stream": false}}'
```

## Deployment

Deploy to Databricks Apps:
```bash
./deploy.sh
```

Or manually:
```bash
# Sync code
databricks sync . /Users/your.name/{project_name}

# Deploy app
databricks apps deploy {project_name} \\
  --source-code-path /Workspace/Users/your.name/{project_name}
```

## Development

Edit `src/agent.py` to implement your agent logic:
- Add tools and integrations
- Configure LLM parameters
- Implement custom prompts
- Add authentication

## MLflow Tracing

All agent interactions are automatically traced with MLflow. View traces in the Databricks workspace under the MLflow UI.
'''
    
    (project_path / "README.md").write_text(readme)
    print("✅ Created README.md")
    
    # Create .gitignore
    gitignore = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# MLflow
mlruns/
mlartifacts/

# Databricks
.databricks/

# OS
.DS_Store
'''
    
    (project_path / ".gitignore").write_text(gitignore)
    print("✅ Created .gitignore")
    
    # Create test file
    test_code = '''"""
Unit tests for agent
"""
import pytest
from src.agent import agent


def test_agent_invoke():
    """Test non-streaming invoke"""
    messages = [{"role": "user", "content": "Hello"}]
    response = agent.invoke(messages)
    assert isinstance(response, str)
    assert len(response) > 0


def test_agent_stream():
    """Test streaming invoke"""
    messages = [{"role": "user", "content": "Hello"}]
    chunks = list(agent.stream(messages))
    assert len(chunks) > 0
    assert all(isinstance(chunk, str) for chunk in chunks)
'''
    
    (project_path / "tests" / "test_agent.py").write_text(test_code)
    print("✅ Created tests/test_agent.py")
    
    print(f"\n✨ Agent project '{project_name}' created successfully at {project_path}")
    print("\nNext steps:")
    print(f"1. cd {project_name}")
    print("2. Edit src/agent.py to implement your agent logic")
    print("3. Test locally: python server.py")
    print("4. Deploy: ./deploy.sh")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python init_agent_project.py <project_name> [output_dir]")
        sys.exit(1)
    
    project_name = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    
    create_agent_project(project_name, output_dir)
