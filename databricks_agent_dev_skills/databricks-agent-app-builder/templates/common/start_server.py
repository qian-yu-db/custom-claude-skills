import logging

from dotenv import load_dotenv
from mlflow.genai.agent_server import AgentServer, setup_mlflow_git_based_version_tracking

# Load env vars from .env.local before importing the agent for proper auth
load_dotenv(dotenv_path=".env.local", override=True)

# Need to import the agent to register the functions with the server
import agent_server.agent  # noqa: E402

# For conversational agents (LangGraph, OpenAI Agents SDK):
agent_server = AgentServer("ResponsesAgent", enable_chat_proxy=True)

# For non-conversational agents, use:
# agent_server = AgentServer()

# Define the app as a module level variable to enable multiple workers
app = agent_server.app  # noqa: F841

# Git-based version tracking may fail in deployed environments (no .git directory)
try:
    setup_mlflow_git_based_version_tracking()
except Exception as e:
    logging.warning(f"Git-based version tracking not available: {e}")


def main():
    agent_server.run(app_import_string="agent_server.start_server:app")
