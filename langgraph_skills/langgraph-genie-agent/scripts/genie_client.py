#!/usr/bin/env python3
"""
Databricks Genie API Client

Provides a Python interface to the Databricks Genie Conversation API.
"""

import os
import time
import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class GenieMessage:
    """Represents a message in a Genie conversation."""
    id: str
    content: str
    status: str
    query_result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class GenieClient:
    """Client for Databricks Genie API."""

    def __init__(
        self,
        host: Optional[str] = None,
        token: Optional[str] = None,
        timeout: int = 60
    ):
        """
        Initialize Genie client.

        Args:
            host: Databricks workspace URL (default: from DATABRICKS_HOST env var)
            token: Databricks personal access token (default: from DATABRICKS_TOKEN env var)
            timeout: Maximum time to wait for query completion in seconds
        """
        self.host = (host or os.getenv("DATABRICKS_HOST", "")).rstrip("/")
        self.token = token or os.getenv("DATABRICKS_TOKEN", "")

        if not self.host:
            raise ValueError("Databricks host must be provided or set in DATABRICKS_HOST env var")
        if not self.token:
            raise ValueError("Databricks token must be provided or set in DATABRICKS_TOKEN env var")

        self.timeout = timeout
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def start_conversation(
        self,
        space_id: str,
        content: str,
        wait_for_completion: bool = True
    ) -> GenieMessage:
        """
        Start a new conversation with a Genie space.

        Args:
            space_id: The Genie space ID
            content: The question or query to ask
            wait_for_completion: Whether to wait for query completion

        Returns:
            GenieMessage with conversation and message IDs

        Raises:
            requests.HTTPError: If API request fails
            TimeoutError: If query doesn't complete within timeout
        """
        url = f"{self.host}/api/2.0/genie/spaces/{space_id}/start-conversation"

        payload = {"content": content}

        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()

        data = response.json()

        conversation_id = data["conversation_id"]
        message_id = data["message_id"]

        if wait_for_completion:
            return self._wait_for_completion(space_id, conversation_id, message_id)
        else:
            return GenieMessage(
                id=message_id,
                content=content,
                status=data.get("status", "PENDING")
            )

    def continue_conversation(
        self,
        space_id: str,
        conversation_id: str,
        content: str,
        wait_for_completion: bool = True
    ) -> GenieMessage:
        """
        Continue an existing conversation.

        Args:
            space_id: The Genie space ID
            conversation_id: Existing conversation ID
            content: The follow-up question or query
            wait_for_completion: Whether to wait for query completion

        Returns:
            GenieMessage with updated conversation state
        """
        url = f"{self.host}/api/2.0/genie/spaces/{space_id}/conversations/{conversation_id}/messages"

        payload = {"content": content}

        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()

        data = response.json()
        message_id = data["id"]

        if wait_for_completion:
            return self._wait_for_completion(space_id, conversation_id, message_id)
        else:
            return GenieMessage(
                id=message_id,
                content=content,
                status=data.get("status", "PENDING")
            )

    def get_message(
        self,
        space_id: str,
        conversation_id: str,
        message_id: str
    ) -> GenieMessage:
        """
        Get a specific message from a conversation.

        Args:
            space_id: The Genie space ID
            conversation_id: The conversation ID
            message_id: The message ID

        Returns:
            GenieMessage with current status and results
        """
        url = f"{self.host}/api/2.0/genie/spaces/{space_id}/conversations/{conversation_id}/messages/{message_id}"

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        data = response.json()

        return GenieMessage(
            id=data["id"],
            content=data.get("content", ""),
            status=data.get("status", "UNKNOWN"),
            query_result=data.get("query_result"),
            error=data.get("error")
        )

    def get_conversation_history(
        self,
        space_id: str,
        conversation_id: str
    ) -> List[GenieMessage]:
        """
        Get full conversation history.

        Args:
            space_id: The Genie space ID
            conversation_id: The conversation ID

        Returns:
            List of GenieMessage objects
        """
        url = f"{self.host}/api/2.0/genie/spaces/{space_id}/conversations/{conversation_id}/messages"

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        messages_data = response.json().get("messages", [])

        return [
            GenieMessage(
                id=msg["id"],
                content=msg.get("content", ""),
                status=msg.get("status", "UNKNOWN"),
                query_result=msg.get("query_result"),
                error=msg.get("error")
            )
            for msg in messages_data
        ]

    def _wait_for_completion(
        self,
        space_id: str,
        conversation_id: str,
        message_id: str
    ) -> GenieMessage:
        """
        Poll for query completion.

        Args:
            space_id: The Genie space ID
            conversation_id: The conversation ID
            message_id: The message ID

        Returns:
            Completed GenieMessage

        Raises:
            TimeoutError: If query doesn't complete within timeout
            Exception: If query fails
        """
        start_time = time.time()
        poll_interval = 2  # seconds

        while time.time() - start_time < self.timeout:
            message = self.get_message(space_id, conversation_id, message_id)

            if message.status == "COMPLETED":
                return message
            elif message.status == "FAILED":
                error_msg = message.error or "Genie query failed"
                raise Exception(f"Genie query failed: {error_msg}")
            elif message.status in ["EXECUTING_QUERY", "PENDING", "FETCHING_METADATA"]:
                # Still processing
                time.sleep(poll_interval)
            else:
                # Unknown status
                print(f"Warning: Unknown status '{message.status}', continuing to wait...")
                time.sleep(poll_interval)

        raise TimeoutError(f"Genie query timed out after {self.timeout} seconds")

    def extract_data(self, message: GenieMessage) -> Dict[str, Any]:
        """
        Extract structured data from a completed Genie message.

        Args:
            message: Completed GenieMessage with query_result

        Returns:
            Dictionary with columns, data, and metadata
        """
        if not message.query_result:
            return {"error": "No query result available"}

        try:
            statement_response = message.query_result.get("statement_response", {})

            # Check status
            status = statement_response.get("status", {})
            if status.get("state") != "SUCCEEDED":
                return {"error": f"Query state: {status.get('state')}"}

            # Get schema
            manifest = statement_response.get("manifest", {})
            schema = manifest.get("schema", {})
            columns = [col["name"] for col in schema.get("columns", [])]

            # Get data
            result = statement_response.get("result", {})
            data_array = result.get("data_array", [])

            # Convert to list of dicts
            records = []
            for row in data_array:
                record = dict(zip(columns, row))
                records.append(record)

            return {
                "columns": columns,
                "data": records,
                "row_count": len(records),
                "truncated": result.get("truncated", False)
            }

        except Exception as e:
            return {
                "error": f"Failed to extract data: {str(e)}",
                "raw_response": message.query_result
            }


def format_as_markdown_table(data: Dict[str, Any], max_rows: int = 10) -> str:
    """
    Format extracted data as a markdown table.

    Args:
        data: Dictionary from extract_data()
        max_rows: Maximum number of rows to display

    Returns:
        Formatted markdown table string
    """
    if "error" in data:
        return f"**Error**: {data['error']}"

    columns = data.get("columns", [])
    records = data.get("data", [])
    row_count = data.get("row_count", 0)

    if row_count == 0:
        return "*No results found*"

    # Create header
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"

    # Create rows
    rows = []
    for record in records[:max_rows]:
        values = [str(record.get(col, "")) for col in columns]
        row = "| " + " | ".join(values) + " |"
        rows.append(row)

    table = "\n".join([header, separator] + rows)

    # Add footer if truncated
    if row_count > max_rows:
        table += f"\n\n*Showing {max_rows} of {row_count} rows*"

    if data.get("truncated"):
        table += "\n\n*Note: Results were truncated by Genie*"

    return table


# Example usage
if __name__ == "__main__":
    import sys

    # Example: Query a Genie space
    if len(sys.argv) < 3:
        print("Usage: python genie_client.py <space_id> <query>")
        sys.exit(1)

    space_id = sys.argv[1]
    query = sys.argv[2]

    client = GenieClient()

    print(f"Querying Genie space '{space_id}'...")
    print(f"Query: {query}\n")

    try:
        message = client.start_conversation(space_id, query)

        print(f"Status: {message.status}")
        print(f"Message ID: {message.id}\n")

        if message.status == "COMPLETED":
            data = client.extract_data(message)
            table = format_as_markdown_table(data)
            print("Results:")
            print(table)
        else:
            print(f"Query did not complete successfully: {message.status}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
