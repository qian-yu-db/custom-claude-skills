#!/usr/bin/env python3
"""
Databricks Vector Search Retriever for LangChain

This module provides a custom retriever that integrates Databricks Vector Search
with LangChain for RAG applications.
"""

import os
from typing import List, Optional, Dict, Any
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from databricks.vector_search.client import VectorSearchClient
from pydantic import Field


def extract_rows(results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract rows from Vector Search results.

    Args:
        results: Raw results from Vector Search API

    Returns:
        List of row dictionaries with columns and values
    """
    if not results or "result" not in results:
        return []

    result_data = results["result"]

    # Handle different result formats
    if "data_array" in result_data:
        # Format: {"data_array": [[val1, val2, ...], ...]}
        columns = result_data.get("columns", [])
        rows = []
        for row_data in result_data["data_array"]:
            row = {col: val for col, val in zip(columns, row_data)}
            rows.append(row)
        return rows
    elif "row_list" in result_data:
        # Format: {"row_list": [{"col1": val1, ...}, ...]}
        return result_data["row_list"]
    else:
        return []


class DatabricksVectorSearchRetriever(BaseRetriever):
    """
    Custom retriever for Databricks Vector Search.

    This retriever integrates with Databricks Vector Search indexes to provide
    semantic search capabilities for RAG applications.

    Attributes:
        index_name: Full name of the Vector Search index (catalog.schema.index)
        endpoint_name: Name of the Vector Search endpoint
        text_column: Column containing the text content (default: "text")
        columns: List of columns to retrieve (default: ["text"])
        num_results: Number of results to return (default: 5)
        filters: Optional filters in JSON format
        workspace_url: Databricks workspace URL (from env if not provided)
        personal_access_token: Databricks PAT (from env if not provided)
    """

    index_name: str = Field(..., description="Full name of Vector Search index")
    endpoint_name: str = Field(..., description="Name of Vector Search endpoint")
    text_column: str = Field(default="text", description="Column containing text")
    columns: List[str] = Field(default_factory=lambda: ["text"], description="Columns to retrieve")
    num_results: int = Field(default=5, description="Number of results to return")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Optional filters")
    workspace_url: Optional[str] = Field(default=None, description="Databricks workspace URL")
    personal_access_token: Optional[str] = Field(default=None, description="Databricks PAT")

    _client: Optional[VectorSearchClient] = None

    def __init__(self, **data):
        """Initialize the retriever."""
        super().__init__(**data)

        # Set workspace URL and token from environment if not provided
        if not self.workspace_url:
            self.workspace_url = os.getenv("DATABRICKS_HOST")
        if not self.personal_access_token:
            self.personal_access_token = os.getenv("DATABRICKS_TOKEN")

        # Initialize Vector Search client
        self._client = VectorSearchClient(
            workspace_url=self.workspace_url,
            personal_access_token=self.personal_access_token,
            disable_notice=True
        )

    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        """
        Retrieve documents from Vector Search.

        Args:
            query: The search query
            run_manager: Callback manager for retriever run

        Returns:
            List of LangChain Document objects
        """
        if not self._client:
            raise RuntimeError("Vector Search client not initialized")

        # Get index
        index = self._client.get_index(
            endpoint_name=self.endpoint_name,
            index_name=self.index_name
        )

        # Prepare columns to retrieve (include score)
        retrieve_columns = list(self.columns)
        if "score" not in retrieve_columns:
            retrieve_columns.append("score")

        # Execute similarity search
        search_kwargs = {
            "query_text": query,
            "columns": retrieve_columns,
            "num_results": self.num_results
        }

        if self.filters:
            search_kwargs["filters"] = self.filters

        results = index.similarity_search(**search_kwargs)

        # Convert to LangChain Documents
        documents = []
        for row in extract_rows(results):
            # Extract text content
            page_content = row.get(self.text_column, "")

            # Build metadata from other columns
            metadata = {
                k: v for k, v in row.items()
                if k != self.text_column
            }

            doc = Document(
                page_content=page_content,
                metadata=metadata
            )
            documents.append(doc)

        return documents


class DatabricksVectorSearchTool:
    """
    LangChain Tool wrapper for Databricks Vector Search.

    This provides a tool interface that can be used with LangGraph agents.
    """

    def __init__(
        self,
        retriever: DatabricksVectorSearchRetriever,
        name: str = "vector_search",
        description: str = "Search knowledge base for relevant information"
    ):
        """
        Initialize the tool.

        Args:
            retriever: The Vector Search retriever instance
            name: Name of the tool
            description: Description shown to the LLM
        """
        self.retriever = retriever
        self.name = name
        self.description = description

    def __call__(self, query: str) -> str:
        """
        Execute the tool.

        Args:
            query: The search query

        Returns:
            Formatted search results as a string
        """
        documents = self.retriever.get_relevant_documents(query)

        if not documents:
            return "No relevant documents found."

        # Format results
        result_parts = []
        for i, doc in enumerate(documents, 1):
            score = doc.metadata.get("score", 0.0)
            source = doc.metadata.get("source", "Unknown")

            result_parts.append(
                f"**Result {i}** (score: {score:.3f}, source: {source}):\n{doc.page_content}"
            )

        return "\n\n".join(result_parts)

    def as_langchain_tool(self):
        """
        Convert to LangChain Tool object.

        Returns:
            LangChain Tool instance
        """
        from langchain_core.tools import Tool

        return Tool(
            name=self.name,
            description=self.description,
            func=self.__call__
        )


def create_retriever(
    index_name: str,
    endpoint_name: str,
    text_column: str = "text",
    columns: Optional[List[str]] = None,
    num_results: int = 5,
    filters: Optional[Dict[str, Any]] = None
) -> DatabricksVectorSearchRetriever:
    """
    Factory function to create a Vector Search retriever.

    Args:
        index_name: Full name of the Vector Search index
        endpoint_name: Name of the Vector Search endpoint
        text_column: Column containing text content
        columns: Columns to retrieve
        num_results: Number of results to return
        filters: Optional filters

    Returns:
        Configured DatabricksVectorSearchRetriever instance
    """
    if columns is None:
        columns = [text_column]

    return DatabricksVectorSearchRetriever(
        index_name=index_name,
        endpoint_name=endpoint_name,
        text_column=text_column,
        columns=columns,
        num_results=num_results,
        filters=filters
    )


def create_vector_search_tool(
    index_name: str,
    endpoint_name: str,
    text_column: str = "text",
    columns: Optional[List[str]] = None,
    num_results: int = 5,
    tool_name: str = "vector_search",
    tool_description: str = "Search knowledge base for relevant information"
):
    """
    Factory function to create a Vector Search tool.

    Args:
        index_name: Full name of the Vector Search index
        endpoint_name: Name of the Vector Search endpoint
        text_column: Column containing text content
        columns: Columns to retrieve
        num_results: Number of results to return
        tool_name: Name of the tool
        tool_description: Description shown to the LLM

    Returns:
        LangChain Tool instance
    """
    retriever = create_retriever(
        index_name=index_name,
        endpoint_name=endpoint_name,
        text_column=text_column,
        columns=columns,
        num_results=num_results
    )

    tool_wrapper = DatabricksVectorSearchTool(
        retriever=retriever,
        name=tool_name,
        description=tool_description
    )

    return tool_wrapper.as_langchain_tool()


# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 4:
        print("Usage: python vector_search_retriever.py <endpoint_name> <index_name> <query>")
        print("\nExample:")
        print('  python vector_search_retriever.py my_endpoint catalog.schema.my_index "What is RAG?"')
        sys.exit(1)

    endpoint_name = sys.argv[1]
    index_name = sys.argv[2]
    query = sys.argv[3]

    # Create retriever
    retriever = create_retriever(
        index_name=index_name,
        endpoint_name=endpoint_name,
        num_results=3
    )

    # Execute search
    print(f"\nSearching for: {query}\n")
    documents = retriever.get_relevant_documents(query)

    # Print results
    if not documents:
        print("No results found.")
    else:
        for i, doc in enumerate(documents, 1):
            score = doc.metadata.get("score", 0.0)
            source = doc.metadata.get("source", "Unknown")
            print(f"Result {i} (score: {score:.3f}, source: {source}):")
            print(doc.page_content)
            print("-" * 60)
