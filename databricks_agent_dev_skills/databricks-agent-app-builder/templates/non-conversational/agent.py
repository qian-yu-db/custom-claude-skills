"""Non-conversational agent for stateless task processing using MLflow model serving."""

import json
import os

from databricks.sdk import WorkspaceClient
from mlflow.genai.agent_server import invoke
from pydantic import BaseModel, Field

w = WorkspaceClient()
openai_client = w.serving_endpoints.get_open_ai_client()


# Define your input schema
class AgentInput(BaseModel):
    document_text: str = Field(..., description="The document text to analyze")
    questions: list[str] = Field(..., description="List of questions to answer")


# Define your output schema
class AnalysisResult(BaseModel):
    question_text: str = Field(..., description="Original question text")
    answer: str = Field(..., description="The answer")
    reasoning: str = Field(..., description="Step-by-step reasoning for the answer")


class AgentOutput(BaseModel):
    results: list[AnalysisResult] = Field(..., description="List of analysis results")


def construct_analysis_prompt(question: str, document_text: str) -> str:
    """Construct the prompt for the LLM."""
    return f"""You are a document analysis expert. Answer the following question based on the provided document.

Question: "{question}"

Document:
{document_text}

Return ONLY a JSON object (no markdown, no code fences, no additional text) with these two fields:
- answer: Your answer to the question
- reasoning: Brief explanation of your reasoning

Example JSON output:
{{
    "answer": "Yes",
    "reasoning": "The document contains evidence that..."
}}
"""


@invoke()
async def invoke(data: dict) -> dict:
    """Process document analysis questions and generate answers.

    Args:
        data: Dictionary containing document_text and list of questions

    Returns:
        Dictionary with analysis results for each question
    """
    # Parse input
    input_data = AgentInput(**data)

    analysis_results = []

    # Process each question
    for question in input_data.questions:
        # Construct prompt
        prompt = construct_analysis_prompt(question, input_data.document_text)

        # Call LLM
        llm_response = openai_client.chat.completions.create(
            model=os.getenv("LLM_MODEL", "databricks-claude-3-7-sonnet"),
            messages=[{"role": "user", "content": prompt}],
        )

        # Parse response
        response_text = llm_response.choices[0].message.content
        try:
            response_data: dict = json.loads(response_text)
            answer = response_data.get("answer", "Unable to determine")
            reasoning = response_data.get("reasoning", "")
        except json.JSONDecodeError as e:
            answer = "Error"
            reasoning = f"Unable to parse LLM response: {e}"

        analysis_results.append(
            AnalysisResult(
                question_text=question,
                answer=answer,
                reasoning=reasoning,
            )
        )

    # Return output
    output = AgentOutput(results=analysis_results)
    return output.model_dump()
