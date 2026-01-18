import asyncio

import mlflow
from dotenv import load_dotenv
from mlflow.genai.agent_server import get_invoke_function
from mlflow.genai.scorers import Safety

# Load environment variables from .env.local if it exists
load_dotenv(dotenv_path=".env.local", override=True)

# Need to import agent for our @invoke-registered function to be found
from agent_server import agent  # noqa: F401

# Create your evaluation dataset
# For non-conversational agents, use the custom input format
eval_dataset = [
    {
        "inputs": {
            "data": {
                "document_text": "The company reported revenue of $10 million in Q3 2024.",
                "questions": ["Does the document mention revenue?"]
            }
        }
    }
]

# Get the invoke function that was registered via @invoke decorator in your agent
invoke_fn = get_invoke_function()
assert invoke_fn is not None, (
    "No function registered with the `@invoke` decorator found."
    "Ensure you have a function decorated with `@invoke()`."
)

# If invoke function is async, wrap it in a sync function
if asyncio.iscoroutinefunction(invoke_fn):

    def sync_invoke_fn(data: dict) -> dict:
        return asyncio.run(invoke_fn(data))
else:
    sync_invoke_fn = invoke_fn


def evaluate():
    mlflow.genai.evaluate(
        data=eval_dataset,
        predict_fn=sync_invoke_fn,
        scorers=[Safety()],
    )
