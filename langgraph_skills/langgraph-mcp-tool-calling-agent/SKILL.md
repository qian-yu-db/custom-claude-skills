# LangGraph MCP Tool-Calling Agent Skill

## Purpose

This skill helps Claude build LangGraph agents that use MCP (Model Context Protocol) tools, including both Databricks managed MCP services and external MCP servers. MCP enables agents to access external data sources, APIs, and services through a standardized protocol.

## When to Activate

This skill should activate when the user requests:
- "Create an MCP tool-calling agent"
- "Build a LangGraph agent with MCP tools"
- "Set up an agent using Databricks managed MCP"
- "Connect to external MCP servers from my agent"
- "Create an agent that uses file system, GitHub, or other MCP tools"
- "Build an agent with Model Context Protocol integration"

## Core Capabilities

### 1. Databricks Managed MCP
- Pre-configured MCP servers managed by Databricks
- Built-in tools (file system, git, database, web, etc.)
- Automatic authentication and access control
- Unity Catalog integration
- No server management required

### 2. External MCP Servers
- Connect to third-party MCP servers
- Custom MCP server integration
- SSE (Server-Sent Events) or stdio transport
- Authentication configuration
- Tool discovery and registration

### 3. Tool-Calling Agents
- LLM decides when to use tools
- Multi-tool coordination
- Tool result processing
- Error handling and retries
- Conversation flow management

### 4. LangGraph Integration
- State management
- Conditional tool execution
- Multi-turn conversations
- Result aggregation
- MLflow tracing

## Databricks Managed MCP Overview

### What is Databricks Managed MCP?

Databricks managed MCP provides pre-configured MCP servers that give agents access to various data sources and services without requiring server setup or management.

### Available Managed MCP Tools

1. **File System Tools**:
   - `read_file`: Read file contents
   - `write_file`: Write to files
   - `list_directory`: List directory contents
   - `search_files`: Search for files
   - Access Unity Catalog volumes

2. **Git Tools**:
   - `git_status`: Check repository status
   - `git_diff`: View changes
   - `git_commit`: Create commits
   - `git_log`: View commit history
   - Access Git repos in Workspace

3. **Database Tools**:
   - `execute_query`: Run SQL queries
   - `list_tables`: List available tables
   - `describe_table`: Get table schema
   - Query Unity Catalog tables

4. **Web Tools**:
   - `fetch_url`: Fetch web content
   - `search_web`: Web search
   - Parse and extract content

### Configuration

```python
from databricks.agents import MCPClient

# Initialize Databricks managed MCP
mcp_client = MCPClient(
    server_type="managed",
    tools=["filesystem", "git", "database", "web"]
)

# List available tools
tools = mcp_client.list_tools()

# Tool format:
# {
#     "name": "read_file",
#     "description": "Read contents of a file",
#     "parameters": {
#         "path": {"type": "string", "description": "File path"}
#     }
# }
```

## External MCP Servers

### What are External MCP Servers?

External MCP servers are third-party or custom MCP implementations that provide tools through the MCP protocol.

### Connection Methods

#### 1. SSE (Server-Sent Events)
```python
mcp_client = MCPClient(
    server_type="external",
    transport="sse",
    url="https://mcp-server.example.com",
    headers={
        "Authorization": "Bearer token123"
    }
)
```

#### 2. Stdio (Standard I/O)
```python
mcp_client = MCPClient(
    server_type="external",
    transport="stdio",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-github"]
)
```

### Popular External MCP Servers

1. **GitHub MCP Server**:
   - Create issues, PRs
   - Search repositories
   - Manage branches

2. **Slack MCP Server**:
   - Send messages
   - List channels
   - Search conversations

3. **PostgreSQL MCP Server**:
   - Execute queries
   - List tables
   - Manage connections

4. **Custom MCP Servers**:
   - Your own tool implementations
   - Internal APIs
   - Proprietary data sources

## Agent Patterns

### Pattern 1: Simple MCP Tool-Calling Agent

Agent that uses MCP tools to answer user queries:

```python
from typing import TypedDict, Annotated, Sequence
import operator

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from databricks_langchain import ChatDatabricks
from databricks.agents import MCPClient
import mlflow


# Agent State
class MCPAgentState(TypedDict):
    """State for MCP tool-calling agent."""
    messages: Annotated[Sequence[BaseMessage], operator.add]


# Initialize MCP client
mcp_client = MCPClient(
    server_type="managed",
    tools=["filesystem", "database"]
)

# Get MCP tools
mcp_tools = mcp_client.get_langchain_tools()

# Initialize LLM with tools
llm = ChatDatabricks(
    endpoint=os.getenv("DATABRICKS_LLM_ENDPOINT", "databricks-meta-llama-3-1-70b-instruct"),
    temperature=0.1
)
llm_with_tools = llm.bind_tools(mcp_tools)


def agent_node(state: MCPAgentState) -> MCPAgentState:
    """
    Agent decides whether to use MCP tools or respond directly.
    """
    messages = state["messages"]

    # LLM decides next action
    response = llm_with_tools.invoke(messages)

    return {"messages": [response]}


def should_continue(state: MCPAgentState) -> str:
    """Determine if we should call tools or end."""
    last_message = state["messages"][-1]

    # If LLM called tools, execute them
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    # Otherwise, we're done
    return "end"


# Build agent graph
def create_mcp_agent():
    """Create MCP tool-calling agent."""

    # Create graph
    graph = StateGraph(MCPAgentState)

    # Add nodes
    graph.add_node("agent", agent_node)
    graph.add_node("tools", ToolNode(mcp_tools))

    # Add edges
    graph.set_entry_point("agent")
    graph.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END
        }
    )
    graph.add_edge("tools", "agent")

    # Compile
    return graph.compile()


# Example usage
if __name__ == "__main__":
    # Enable MLflow tracing
    mlflow.langchain.autolog()

    # Create agent
    agent = create_mcp_agent()

    # Run agent
    with mlflow.start_run():
        result = agent.invoke({
            "messages": [HumanMessage(content="What files are in /Volumes/catalog/schema/volume?")]
        })

        # Print conversation
        for msg in result["messages"]:
            if isinstance(msg, HumanMessage):
                print(f"User: {msg.content}")
            elif isinstance(msg, AIMessage):
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    print(f"Agent: [Calling tools: {[tc['name'] for tc in msg.tool_calls]}]")
                else:
                    print(f"Agent: {msg.content}")
            elif isinstance(msg, ToolMessage):
                print(f"Tool: {msg.content[:200]}...")
```

### Pattern 2: Multi-MCP Agent

Agent that combines tools from multiple MCP servers:

```python
class MultiMCPState(TypedDict):
    """State for multi-MCP agent."""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    active_servers: list  # Which MCP servers are active


# Initialize multiple MCP clients
managed_mcp = MCPClient(
    server_type="managed",
    tools=["filesystem", "database"]
)

github_mcp = MCPClient(
    server_type="external",
    transport="stdio",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-github"],
    env={
        "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN")
    }
)

slack_mcp = MCPClient(
    server_type="external",
    transport="sse",
    url="https://slack-mcp.example.com",
    headers={
        "Authorization": f"Bearer {os.getenv('SLACK_TOKEN')}"
    }
)

# Combine tools from all servers
all_tools = (
    managed_mcp.get_langchain_tools() +
    github_mcp.get_langchain_tools() +
    slack_mcp.get_langchain_tools()
)

# Create agent with all tools
llm_with_all_tools = llm.bind_tools(all_tools)


def multi_mcp_agent_node(state: MultiMCPState) -> MultiMCPState:
    """Agent with access to multiple MCP servers."""
    messages = state["messages"]

    # LLM can choose from any available tool
    response = llm_with_all_tools.invoke(messages)

    return {"messages": [response]}


# Build graph
def create_multi_mcp_agent():
    graph = StateGraph(MultiMCPState)

    graph.add_node("agent", multi_mcp_agent_node)
    graph.add_node("tools", ToolNode(all_tools))

    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", should_continue, {
        "tools": "tools",
        "end": END
    })
    graph.add_edge("tools", "agent")

    return graph.compile()
```

### Pattern 3: Conditional MCP Tool Selection

Agent that dynamically selects which MCP tools to use:

```python
class ConditionalMCPState(TypedDict):
    """State for conditional MCP agent."""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    query_type: str  # "filesystem", "git", "database", etc.
    selected_tools: list


def analyze_query_node(state: ConditionalMCPState) -> ConditionalMCPState:
    """Analyze query to determine needed tools."""
    user_query = state["messages"][-1].content

    analysis_prompt = f"""Analyze this query to determine which tool categories are needed:

Query: {user_query}

Categories:
- filesystem: File operations, reading/writing files
- git: Version control operations
- database: SQL queries, table operations
- web: Web searches, URL fetching
- github: GitHub API operations

Return comma-separated categories:"""

    response = llm.invoke(analysis_prompt)
    categories = [c.strip() for c in response.content.split(",")]

    # Select tools based on categories
    selected_tools = []
    for category in categories:
        if category == "filesystem":
            selected_tools.extend(managed_mcp.get_tools(category="filesystem"))
        elif category == "git":
            selected_tools.extend(managed_mcp.get_tools(category="git"))
        elif category == "database":
            selected_tools.extend(managed_mcp.get_tools(category="database"))
        elif category == "github":
            selected_tools.extend(github_mcp.get_tools())

    return {
        "query_type": ", ".join(categories),
        "selected_tools": selected_tools
    }


def execute_with_selected_tools_node(state: ConditionalMCPState) -> ConditionalMCPState:
    """Execute agent with only selected tools."""
    selected_tools = state["selected_tools"]

    # Create LLM with only selected tools
    llm_with_selected = llm.bind_tools(selected_tools)

    messages = state["messages"]
    response = llm_with_selected.invoke(messages)

    return {"messages": [response]}


# Build graph
def create_conditional_mcp_agent():
    graph = StateGraph(ConditionalMCPState)

    graph.add_node("analyze_query", analyze_query_node)
    graph.add_node("execute", execute_with_selected_tools_node)
    graph.add_node("tools", lambda state: ToolNode(state["selected_tools"])(state))

    graph.set_entry_point("analyze_query")
    graph.add_edge("analyze_query", "execute")
    graph.add_conditional_edges("execute", should_continue, {
        "tools": "tools",
        "end": END
    })
    graph.add_edge("tools", "execute")

    return graph.compile()
```

### Pattern 4: MCP + RAG Hybrid Agent

Combine MCP tools with RAG retrieval:

```python
from vector_search_retriever import create_retriever

class HybridState(TypedDict):
    """State for hybrid MCP + RAG agent."""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    needs_tools: bool
    needs_retrieval: bool
    retrieved_docs: list
    tool_results: list


# Initialize components
mcp_client = MCPClient(server_type="managed", tools=["filesystem", "database"])
mcp_tools = mcp_client.get_langchain_tools()

retriever = create_retriever(
    index_name="catalog.schema.docs_index",
    endpoint_name="my_endpoint"
)

llm_with_tools = llm.bind_tools(mcp_tools)


def analyze_needs_node(state: HybridState) -> HybridState:
    """Determine if query needs tools, retrieval, or both."""
    query = state["messages"][-1].content

    analysis_prompt = f"""Analyze this query:

Query: {query}

Does it need:
1. MCP tools (file operations, database queries, etc.)? YES/NO
2. Document retrieval (documentation, guides, etc.)? YES/NO

Format: TOOLS: YES/NO, RETRIEVAL: YES/NO"""

    response = llm.invoke(analysis_prompt)
    content = response.content.upper()

    needs_tools = "TOOLS: YES" in content
    needs_retrieval = "RETRIEVAL: YES" in content

    return {
        "needs_tools": needs_tools,
        "needs_retrieval": needs_retrieval
    }


def retrieve_node(state: HybridState) -> HybridState:
    """Retrieve documents if needed."""
    if not state.get("needs_retrieval", False):
        return state

    query = state["messages"][-1].content
    docs = retriever.get_relevant_documents(query)

    return {"retrieved_docs": docs}


def agent_with_context_node(state: HybridState) -> HybridState:
    """Agent with retrieval context and tools."""
    messages = list(state["messages"])

    # Add retrieval context if available
    if state.get("retrieved_docs"):
        context = "\n\n".join([doc.page_content for doc in state["retrieved_docs"]])
        context_msg = SystemMessage(content=f"Retrieved context:\n{context}")
        messages.insert(-1, context_msg)

    # LLM with tools
    response = llm_with_tools.invoke(messages)

    return {"messages": [response]}


# Build hybrid graph
def create_hybrid_agent():
    graph = StateGraph(HybridState)

    graph.add_node("analyze_needs", analyze_needs_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("agent", agent_with_context_node)
    graph.add_node("tools", ToolNode(mcp_tools))

    graph.set_entry_point("analyze_needs")
    graph.add_edge("analyze_needs", "retrieve")
    graph.add_edge("retrieve", "agent")
    graph.add_conditional_edges("agent", should_continue, {
        "tools": "tools",
        "end": END
    })
    graph.add_edge("tools", "agent")

    return graph.compile()
```

## MCP Client Implementation

### Databricks Managed MCP

```python
from databricks.sdk import WorkspaceClient
from typing import List, Dict, Any, Optional


class DatabricksManagedMCP:
    """Client for Databricks managed MCP services."""

    def __init__(self, workspace_url: Optional[str] = None, token: Optional[str] = None):
        """
        Initialize Databricks managed MCP client.

        Args:
            workspace_url: Databricks workspace URL
            token: Personal access token
        """
        self.workspace_url = workspace_url or os.getenv("DATABRICKS_HOST")
        self.token = token or os.getenv("DATABRICKS_TOKEN")

        # Initialize Workspace client
        self.client = WorkspaceClient(
            host=self.workspace_url,
            token=self.token
        )

    def list_available_tools(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List available managed MCP tools.

        Args:
            category: Filter by category (filesystem, git, database, web)

        Returns:
            List of tool specifications
        """
        # Call Databricks API to list tools
        response = self.client.api_client.do(
            "GET",
            "/api/2.0/mcp/managed/tools",
            query={"category": category} if category else None
        )

        return response.get("tools", [])

    def call_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Call a managed MCP tool.

        Args:
            tool_name: Name of the tool
            arguments: Tool arguments

        Returns:
            Tool execution result
        """
        response = self.client.api_client.do(
            "POST",
            "/api/2.0/mcp/managed/tools/execute",
            data={
                "tool_name": tool_name,
                "arguments": arguments
            }
        )

        return response

    def get_langchain_tools(self, category: Optional[str] = None):
        """
        Get LangChain Tool objects for managed MCP.

        Args:
            category: Filter by category

        Returns:
            List of LangChain Tool objects
        """
        from langchain_core.tools import Tool

        tools = self.list_available_tools(category)

        langchain_tools = []
        for tool_spec in tools:
            def make_tool_func(tool_name):
                def tool_func(**kwargs):
                    return self.call_tool(tool_name, kwargs)
                return tool_func

            langchain_tool = Tool(
                name=tool_spec["name"],
                description=tool_spec["description"],
                func=make_tool_func(tool_spec["name"])
            )
            langchain_tools.append(langchain_tool)

        return langchain_tools
```

### External MCP Client

```python
import asyncio
import json
from typing import List, Dict, Any, Optional


class ExternalMCPClient:
    """Client for external MCP servers."""

    def __init__(
        self,
        transport: str = "sse",
        url: Optional[str] = None,
        command: Optional[str] = None,
        args: Optional[List[str]] = None,
        env: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None
    ):
        """
        Initialize external MCP client.

        Args:
            transport: "sse" or "stdio"
            url: Server URL (for SSE)
            command: Command to run (for stdio)
            args: Command arguments (for stdio)
            env: Environment variables
            headers: HTTP headers (for SSE)
        """
        self.transport = transport
        self.url = url
        self.command = command
        self.args = args or []
        self.env = env or {}
        self.headers = headers or {}

        self.tools = []
        self.connection = None

    async def connect(self):
        """Connect to the MCP server."""
        if self.transport == "sse":
            await self._connect_sse()
        elif self.transport == "stdio":
            await self._connect_stdio()
        else:
            raise ValueError(f"Unknown transport: {self.transport}")

        # List tools after connection
        await self._list_tools()

    async def _connect_sse(self):
        """Connect via SSE."""
        import aiohttp

        self.session = aiohttp.ClientSession()
        self.connection = await self.session.get(
            self.url,
            headers=self.headers
        )

    async def _connect_stdio(self):
        """Connect via stdio."""
        self.process = await asyncio.create_subprocess_exec(
            self.command,
            *self.args,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env={**os.environ, **self.env}
        )
        self.connection = self.process

    async def _list_tools(self):
        """List available tools from the server."""
        # Send list_tools request
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list"
        }

        response = await self._send_request(request)
        self.tools = response.get("result", {}).get("tools", [])

    async def _send_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Send request to MCP server."""
        if self.transport == "sse":
            return await self._send_sse_request(request)
        elif self.transport == "stdio":
            return await self._send_stdio_request(request)

    async def _send_stdio_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Send request via stdio."""
        # Write request
        request_str = json.dumps(request) + "\n"
        self.process.stdin.write(request_str.encode())
        await self.process.stdin.drain()

        # Read response
        response_str = await self.process.stdout.readline()
        response = json.loads(response_str)

        return response

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Call an MCP tool."""
        request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }

        response = await self._send_request(request)
        return response.get("result")

    def get_langchain_tools(self):
        """Get LangChain Tool objects."""
        from langchain_core.tools import Tool

        langchain_tools = []
        for tool_spec in self.tools:
            def make_tool_func(tool_name):
                def tool_func(**kwargs):
                    loop = asyncio.get_event_loop()
                    return loop.run_until_complete(self.call_tool(tool_name, kwargs))
                return tool_func

            langchain_tool = Tool(
                name=tool_spec["name"],
                description=tool_spec.get("description", ""),
                func=make_tool_func(tool_spec["name"])
            )
            langchain_tools.append(langchain_tool)

        return langchain_tools
```

## Configuration Management

### MCP Configuration File

```json
{
  "mcp_servers": {
    "managed": {
      "type": "managed",
      "enabled": true,
      "tools": ["filesystem", "git", "database", "web"],
      "config": {
        "workspace_url": "${DATABRICKS_HOST}",
        "token": "${DATABRICKS_TOKEN}"
      }
    },
    "github": {
      "type": "external",
      "enabled": true,
      "transport": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "slack": {
      "type": "external",
      "enabled": true,
      "transport": "sse",
      "url": "https://slack-mcp.example.com",
      "headers": {
        "Authorization": "Bearer ${SLACK_TOKEN}"
      }
    }
  },
  "agent": {
    "llm_endpoint": "databricks-meta-llama-3-1-70b-instruct",
    "temperature": 0.1,
    "enable_tracing": true,
    "max_iterations": 10
  }
}
```

## Best Practices

1. **Tool Selection**:
   - Start with minimal tools needed
   - Add more tools as requirements grow
   - Use conditional tool loading for performance

2. **Error Handling**:
   - Handle tool failures gracefully
   - Implement retries for transient errors
   - Provide fallback responses

3. **Security**:
   - Use environment variables for secrets
   - Validate tool arguments
   - Implement access controls
   - Audit tool usage

4. **Performance**:
   - Cache tool results when appropriate
   - Use async operations
   - Monitor tool execution time
   - Set reasonable timeouts

5. **Observability**:
   - Enable MLflow tracing
   - Log tool calls and results
   - Monitor error rates
   - Track tool usage metrics

## References

- Databricks Managed MCP: https://docs.databricks.com/aws/en/generative-ai/mcp/managed-mcp
- External MCP Servers: https://docs.databricks.com/aws/en/generative-ai/mcp/external-mcp
- Model Context Protocol: https://modelcontextprotocol.io
- MCP Specification: https://spec.modelcontextprotocol.io
