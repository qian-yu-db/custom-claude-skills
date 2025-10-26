#!/usr/bin/env python3
"""
Self-Querying Retriever for Databricks Vector Search

This module implements a self-querying retriever that uses an LLM to extract
structured filters from natural language queries, enabling more precise
Vector Search results.
"""

import os
from typing import List, Optional, Dict, Any, Tuple
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.structured_query import (
    StructuredQuery,
    Comparator,
    Comparison,
    Operation,
    Operator,
    FilterDirective
)
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from databricks.vector_search.client import VectorSearchClient
from databricks_langchain import ChatDatabricks
from pydantic import Field
import json


def extract_rows(results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract rows from Vector Search results.

    Args:
        results: Raw results from Vector Search API

    Returns:
        List of row dictionaries
    """
    if not results or "result" not in results:
        return []

    result_data = results["result"]

    if "data_array" in result_data:
        columns = result_data.get("columns", [])
        rows = []
        for row_data in result_data["data_array"]:
            row = {col: val for col, val in zip(columns, row_data)}
            rows.append(row)
        return rows
    elif "row_list" in result_data:
        return result_data["row_list"]
    else:
        return []


def convert_structured_query_to_databricks_filter(
    structured_query: StructuredQuery
) -> Optional[Dict[str, Any]]:
    """
    Convert LangChain StructuredQuery filter to Databricks Vector Search filter format.

    Args:
        structured_query: The structured query from the LLM

    Returns:
        Databricks Vector Search compatible filter dict
    """
    if not structured_query.filter:
        return None

    def convert_directive(directive: FilterDirective) -> Dict[str, Any]:
        """Convert a filter directive to Databricks format."""
        if isinstance(directive, Comparison):
            # Handle comparison operations
            comparator_map = {
                Comparator.EQ: "$eq",
                Comparator.NE: "$ne",
                Comparator.GT: "$gt",
                Comparator.GTE: "$gte",
                Comparator.LT: "$lt",
                Comparator.LTE: "$lte",
                Comparator.IN: "$in",
                Comparator.NIN: "$nin",
                Comparator.LIKE: "$like",
                Comparator.CONTAIN: "$contains"
            }

            databricks_comparator = comparator_map.get(directive.comparator)
            if not databricks_comparator:
                raise ValueError(f"Unsupported comparator: {directive.comparator}")

            return {
                directive.attribute: {
                    databricks_comparator: directive.value
                }
            }

        elif isinstance(directive, Operation):
            # Handle logical operations (AND, OR, NOT)
            operator_map = {
                Operator.AND: "$and",
                Operator.OR: "$or",
                Operator.NOT: "$not"
            }

            databricks_operator = operator_map.get(directive.operator)
            if not databricks_operator:
                raise ValueError(f"Unsupported operator: {directive.operator}")

            converted_args = [convert_directive(arg) for arg in directive.arguments]

            if databricks_operator == "$not":
                # NOT operator takes a single argument
                return {databricks_operator: converted_args[0]}
            else:
                # AND/OR operators take a list of arguments
                return {databricks_operator: converted_args}

        else:
            raise ValueError(f"Unknown directive type: {type(directive)}")

    return convert_directive(structured_query.filter)


class DatabricksVectorSearchStore:
    """
    Vector store interface for Databricks Vector Search.

    This class provides the interface needed for SelfQueryRetriever.
    """

    def __init__(
        self,
        index_name: str,
        endpoint_name: str,
        text_column: str = "text",
        columns: Optional[List[str]] = None,
        workspace_url: Optional[str] = None,
        personal_access_token: Optional[str] = None
    ):
        """
        Initialize the vector store.

        Args:
            index_name: Full name of Vector Search index
            endpoint_name: Name of Vector Search endpoint
            text_column: Column containing text content
            columns: Columns to retrieve
            workspace_url: Databricks workspace URL
            personal_access_token: Databricks PAT
        """
        self.index_name = index_name
        self.endpoint_name = endpoint_name
        self.text_column = text_column
        self.columns = columns or [text_column]

        # Set workspace URL and token from environment if not provided
        self.workspace_url = workspace_url or os.getenv("DATABRICKS_HOST")
        self.personal_access_token = personal_access_token or os.getenv("DATABRICKS_TOKEN")

        # Initialize Vector Search client
        self.client = VectorSearchClient(
            workspace_url=self.workspace_url,
            personal_access_token=self.personal_access_token,
            disable_notice=True
        )

    def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> List[Document]:
        """
        Perform similarity search with optional filters.

        Args:
            query: Search query
            k: Number of results
            filter: Optional filter dict
            **kwargs: Additional arguments

        Returns:
            List of LangChain Documents
        """
        # Get index
        index = self.client.get_index(
            endpoint_name=self.endpoint_name,
            index_name=self.index_name
        )

        # Prepare columns to retrieve
        retrieve_columns = list(self.columns)
        if "score" not in retrieve_columns:
            retrieve_columns.append("score")

        # Execute search
        search_kwargs = {
            "query_text": query,
            "columns": retrieve_columns,
            "num_results": k
        }

        if filter:
            search_kwargs["filters"] = filter

        results = index.similarity_search(**search_kwargs)

        # Convert to LangChain Documents
        documents = []
        for row in extract_rows(results):
            page_content = row.get(self.text_column, "")
            metadata = {k: v for k, v in row.items() if k != self.text_column}

            doc = Document(
                page_content=page_content,
                metadata=metadata
            )
            documents.append(doc)

        return documents


class DatabricksSelfQueryRetriever(BaseRetriever):
    """
    Self-querying retriever for Databricks Vector Search.

    This retriever uses an LLM to extract structured filters from natural language
    queries, enabling more precise search results.

    Example:
        >>> metadata_field_info = [
        ...     AttributeInfo(
        ...         name="source",
        ...         description="The source document (e.g., 'user_guide.pdf')",
        ...         type="string"
        ...     ),
        ...     AttributeInfo(
        ...         name="page",
        ...         description="The page number in the document",
        ...         type="integer"
        ...     ),
        ...     AttributeInfo(
        ...         name="category",
        ...         description="Document category (tutorial, reference, guide)",
        ...         type="string"
        ...     )
        ... ]
        >>>
        >>> retriever = DatabricksSelfQueryRetriever.from_databricks(
        ...     index_name="catalog.schema.docs_index",
        ...     endpoint_name="my_endpoint",
        ...     document_content_description="Technical documentation and guides",
        ...     metadata_field_info=metadata_field_info
        ... )
        >>>
        >>> # Query with natural language filters
        >>> docs = retriever.get_relevant_documents(
        ...     "Show me tutorials about Vector Search from the user guide"
        ... )
    """

    vector_store: DatabricksVectorSearchStore = Field(..., description="Vector store instance")
    llm: Any = Field(..., description="LLM for query construction")
    document_content_description: str = Field(..., description="Description of document contents")
    metadata_field_info: List[AttributeInfo] = Field(..., description="Metadata field information")
    structured_query_translator: Any = Field(default=None, description="Query translator")
    num_results: int = Field(default=4, description="Number of results to return")
    enable_limit: bool = Field(default=False, description="Enable limit in structured queries")
    verbose: bool = Field(default=False, description="Verbose output")

    def __init__(self, **data):
        """Initialize the self-query retriever."""
        super().__init__(**data)

        # Import here to avoid circular dependencies
        from langchain.chains.query_constructor.base import get_query_constructor_prompt

        # Create query constructor chain
        self.query_constructor_chain = get_query_constructor_prompt(
            document_contents=self.document_content_description,
            attribute_info=self.metadata_field_info,
            enable_limit=self.enable_limit
        ) | self.llm

    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        """
        Retrieve documents using self-querying.

        Args:
            query: Natural language query
            run_manager: Callback manager

        Returns:
            List of relevant documents
        """
        # Step 1: Use LLM to construct structured query
        if self.verbose:
            print(f"Original query: {query}")

        try:
            # Get structured query from LLM
            structured_query_dict = self.query_constructor_chain.invoke({"query": query})

            # Parse structured query
            if isinstance(structured_query_dict, dict):
                structured_query = StructuredQuery(**structured_query_dict)
            else:
                # If LLM returns a StructuredQuery directly
                structured_query = structured_query_dict

            if self.verbose:
                print(f"Structured query: {structured_query}")

            # Step 2: Convert to Databricks filter format
            databricks_filter = None
            if structured_query.filter:
                databricks_filter = convert_structured_query_to_databricks_filter(structured_query)

                if self.verbose:
                    print(f"Databricks filter: {json.dumps(databricks_filter, indent=2)}")

            # Step 3: Execute search with filters
            search_query = structured_query.query or query
            k = structured_query.limit if self.enable_limit and structured_query.limit else self.num_results

            documents = self.vector_store.similarity_search(
                query=search_query,
                k=k,
                filter=databricks_filter
            )

            if self.verbose:
                print(f"Retrieved {len(documents)} documents")

            return documents

        except Exception as e:
            if self.verbose:
                print(f"Error in self-query: {e}")
                print("Falling back to regular similarity search")

            # Fallback to regular search if structured query fails
            return self.vector_store.similarity_search(
                query=query,
                k=self.num_results
            )

    @classmethod
    def from_databricks(
        cls,
        index_name: str,
        endpoint_name: str,
        document_content_description: str,
        metadata_field_info: List[AttributeInfo],
        text_column: str = "text",
        columns: Optional[List[str]] = None,
        llm: Optional[Any] = None,
        num_results: int = 4,
        enable_limit: bool = False,
        verbose: bool = False
    ) -> "DatabricksSelfQueryRetriever":
        """
        Create a self-query retriever from Databricks Vector Search.

        Args:
            index_name: Full name of Vector Search index
            endpoint_name: Name of Vector Search endpoint
            document_content_description: Description of document contents
            metadata_field_info: List of metadata field descriptions
            text_column: Column containing text content
            columns: Columns to retrieve
            llm: LLM for query construction (defaults to Databricks LLM)
            num_results: Number of results to return
            enable_limit: Enable limit in structured queries
            verbose: Enable verbose output

        Returns:
            Configured DatabricksSelfQueryRetriever
        """
        # Initialize vector store
        vector_store = DatabricksVectorSearchStore(
            index_name=index_name,
            endpoint_name=endpoint_name,
            text_column=text_column,
            columns=columns
        )

        # Initialize LLM if not provided
        if llm is None:
            llm = ChatDatabricks(
                endpoint=os.getenv("DATABRICKS_LLM_ENDPOINT", "databricks-meta-llama-3-1-70b-instruct"),
                temperature=0
            )

        return cls(
            vector_store=vector_store,
            llm=llm,
            document_content_description=document_content_description,
            metadata_field_info=metadata_field_info,
            num_results=num_results,
            enable_limit=enable_limit,
            verbose=verbose
        )


# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 4:
        print("Usage: python self_query_retriever.py <endpoint_name> <index_name> <query>")
        print("\nExample:")
        print('  python self_query_retriever.py my_endpoint catalog.schema.docs_index "Show tutorials from user_guide.pdf"')
        sys.exit(1)

    endpoint_name = sys.argv[1]
    index_name = sys.argv[2]
    query = sys.argv[3]

    # Define metadata fields
    metadata_field_info = [
        AttributeInfo(
            name="source",
            description="The source document name",
            type="string"
        ),
        AttributeInfo(
            name="page",
            description="The page number in the document",
            type="integer"
        ),
        AttributeInfo(
            name="category",
            description="Document category (tutorial, reference, guide, api)",
            type="string"
        ),
        AttributeInfo(
            name="date",
            description="Document creation date in YYYY-MM-DD format",
            type="string"
        )
    ]

    # Create self-query retriever
    retriever = DatabricksSelfQueryRetriever.from_databricks(
        index_name=index_name,
        endpoint_name=endpoint_name,
        document_content_description="Technical documentation, tutorials, and API references",
        metadata_field_info=metadata_field_info,
        verbose=True
    )

    # Execute query
    print(f"\nQuerying: {query}\n")
    documents = retriever.get_relevant_documents(query)

    # Print results
    if not documents:
        print("No results found.")
    else:
        print(f"\nFound {len(documents)} documents:\n")
        for i, doc in enumerate(documents, 1):
            print(f"Result {i}:")
            print(f"  Content: {doc.page_content[:200]}...")
            print(f"  Metadata: {doc.metadata}")
            print("-" * 60)
