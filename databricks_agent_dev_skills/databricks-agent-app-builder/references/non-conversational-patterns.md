# Non-Conversational Agent Patterns

Reference for building stateless, task-specific agents on Databricks.

## Overview

Non-conversational agents process discrete requests without maintaining chat history. They're ideal for:
- Document analysis
- Form processing
- Data extraction
- Batch processing tasks
- API-style interactions

## Core Dependencies

```toml
dependencies = [
    "fastapi>=0.115.12",
    "uvicorn[standard]>=0.34.2",
    "mlflow>=3.7.0",
    "databricks-sdk>=0.63.0",
    "pydantic>=2.11",
    "python-dotenv",
]
```

## AgentServer Setup

```python
from mlflow.genai.agent_server import AgentServer

# No agent_type = None (default for non-conversational)
agent_server = AgentServer()

app = agent_server.app

def main():
    agent_server.run(app_import_string="agent_server.start_server:app")
```

## Input/Output Schemas

### Define with Pydantic

```python
from pydantic import BaseModel, Field

class AgentInput(BaseModel):
    document_text: str = Field(..., description="The document text to analyze")
    questions: list[str] = Field(..., description="List of questions to answer")

class AnalysisResult(BaseModel):
    question_text: str = Field(..., description="Original question")
    answer: str = Field(..., description="The answer")
    reasoning: str = Field(..., description="Step-by-step reasoning")

class AgentOutput(BaseModel):
    results: list[AnalysisResult] = Field(..., description="Analysis results")
```

## LLM Client

### Using Databricks SDK

```python
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()
openai_client = w.serving_endpoints.get_open_ai_client()
```

### Making LLM Calls

```python
import os

llm_response = openai_client.chat.completions.create(
    model=os.getenv("LLM_MODEL", "databricks-claude-3-7-sonnet"),
    messages=[{"role": "user", "content": prompt}],
)

response_text = llm_response.choices[0].message.content
```

## Agent Implementation

### Basic Pattern

```python
from mlflow.genai.agent_server import invoke

@invoke()
async def invoke(data: dict) -> dict:
    # Parse input
    input_data = AgentInput(**data)

    # Process
    results = []
    for item in input_data.items:
        result = await process_item(item)
        results.append(result)

    # Return output
    return AgentOutput(results=results).model_dump()
```

### Document Analysis Example

```python
import json
import os
from databricks.sdk import WorkspaceClient
from mlflow.genai.agent_server import invoke
from pydantic import BaseModel, Field

w = WorkspaceClient()
openai_client = w.serving_endpoints.get_open_ai_client()

class AgentInput(BaseModel):
    document_text: str = Field(..., description="Document to analyze")
    questions: list[str] = Field(..., description="Yes/no questions")

class AnalysisResult(BaseModel):
    question_text: str
    answer: str
    reasoning: str

class AgentOutput(BaseModel):
    results: list[AnalysisResult]

def construct_prompt(question: str, document: str) -> str:
    return f"""Analyze the document and answer the question.

Question: "{question}"

Document:
{document}

Return JSON with:
- answer: "Yes" or "No"
- reasoning: Brief explanation

Return ONLY valid JSON, no markdown."""

@invoke()
async def invoke(data: dict) -> dict:
    input_data = AgentInput(**data)
    results = []

    for question in input_data.questions:
        prompt = construct_prompt(question, input_data.document_text)

        response = openai_client.chat.completions.create(
            model=os.getenv("LLM_MODEL", "databricks-claude-3-7-sonnet"),
            messages=[{"role": "user", "content": prompt}],
        )

        response_text = response.choices[0].message.content

        try:
            parsed = json.loads(response_text)
            answer = parsed.get("answer", "No")
            reasoning = parsed.get("reasoning", "")
        except json.JSONDecodeError:
            answer = "No"
            reasoning = "Failed to parse response"

        results.append(AnalysisResult(
            question_text=question,
            answer=answer,
            reasoning=reasoning,
        ))

    return AgentOutput(results=results).model_dump()
```

## API Usage

### Request Format

```bash
curl -X POST http://localhost:8000/invocations \
  -H "Content-Type: application/json" \
  -d '{
    "document_text": "Total assets: $2,300,000. Total liabilities: $1,200,000...",
    "questions": [
      "Does the document contain a balance sheet?",
      "Is the company profitable?"
    ]
  }'
```

### Response Format

```json
{
  "results": [
    {
      "question_text": "Does the document contain a balance sheet?",
      "answer": "Yes",
      "reasoning": "The document lists total assets and liabilities, which are balance sheet components."
    },
    {
      "question_text": "Is the company profitable?",
      "answer": "Yes",
      "reasoning": "Assets ($2.3M) exceed liabilities ($1.2M), indicating positive equity."
    }
  ]
}
```

## Testing

### Local Testing

```python
# test_agent.py
import httpx

def test_agent():
    response = httpx.post(
        "http://localhost:8000/invocations",
        json={
            "document_text": "Test document content...",
            "questions": ["Is this a test?"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
```

### Remote Testing

```python
import httpx
import subprocess

def get_oauth_token():
    result = subprocess.run(["databricks", "auth", "token"], capture_output=True, text=True)
    return result.stdout.strip()

def test_remote(app_url: str):
    token = get_oauth_token()
    response = httpx.post(
        f"{app_url}/invocations",
        headers={"Authorization": f"Bearer {token}"},
        json={"document_text": "...", "questions": ["..."]},
    )
    return response.json()
```

## Evaluation

```python
import mlflow
from mlflow.genai.scorers import Safety

eval_dataset = [
    {
        "inputs": {
            "data": {
                "document_text": "Sample document...",
                "questions": ["Sample question?"]
            }
        }
    }
]

mlflow.genai.evaluate(
    data=eval_dataset,
    predict_fn=invoke_fn,
    scorers=[Safety()],
)
```

## Comparison with Conversational Agents

| Aspect | Non-Conversational | Conversational |
|--------|-------------------|----------------|
| AgentServer | `AgentServer()` | `AgentServer("ResponsesAgent")` |
| Input | Custom Pydantic models | `ResponsesAgentRequest` |
| Output | Custom Pydantic models | `ResponsesAgentResponse` |
| Streaming | No | Yes (`@stream()`) |
| State | Stateless | Can maintain history |
| Use Case | Discrete tasks | Multi-turn chat |

## When to Use Non-Conversational

- Processing discrete, independent requests
- No need for conversation history
- Custom input/output schemas required
- API-style interactions
- Batch processing tasks

## Best Practices

1. **Use Pydantic** for input/output validation
2. **Handle JSON parsing errors** gracefully
3. **Environment variables** for model configuration
4. **Structured prompts** for consistent LLM responses
5. **Unit tests** for each processing step
