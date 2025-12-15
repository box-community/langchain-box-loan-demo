"""Tools for loan underwriting agents.

This module provides LangChain tool wrappers for Box AI functionality
used by the loan underwriting sub-agents.
"""

from langchain_core.tools import tool
from box_ai_agents_toolkit import (
    box_locate_folder_by_name,
    box_folder_items_list,
    box_ai_ask_file_multi,
    box_ai_extract_structured_enhanced_using_fields,
)
from app_config import conf
from utils.box_api_auth import get_box_client


@tool(parse_docstring=True)
def search_loan_folder(applicant_name: str) -> str:
    """Locate a loan application folder in Box by applicant name.

    Args:
        applicant_name: Name of the loan applicant (e.g., "Sarah Chen")

    Returns:
        Folder ID and path information
    """
    try:
        if conf.box_client is None:
            conf.box_client = get_box_client()
        # Search for folder in Box
        parent_folder_id = conf.BOX_DEMO_PARENT_FOLDER
        folder = box_locate_folder_by_name(
            client=conf.box_client,
            folder_name=applicant_name,
            parent_folder_id=parent_folder_id,
        )

        if folder:
            return f"Found folder: {folder.name} (ID: {folder.id})"
        else:
            return f"Folder not found for applicant: {applicant_name}"
    except Exception as e:
        return f"Error searching for folder '{applicant_name}': {str(e)}"


@tool(parse_docstring=True)
def list_loan_documents(folder_id: str) -> str:
    """List all documents in a loan application folder.

    Args:
        folder_id: Box folder ID containing the loan application

    Returns:
        List of files in the folder with names and IDs
    """
    try:
        if conf.box_client is None:
            conf.box_client = get_box_client()
        response = box_folder_items_list(
            client=conf.box_client, folder_id=folder_id, is_recursive=False
        )

        result = f"Documents in folder {folder_id}:\n\n"

        for item in response.get("folder_items", []):
            item_type = "📁" if item.get("type") == "folder" else "📄"
            result += f"{item_type} {item.get('name', 'Unknown')} (ID: {item.get('id', 'N/A')}, Type: {item.get('type', 'N/A')})\n"

        # # The function returns a dict with 'items' key
        # if isinstance(response, dict) and "items" in response:
        #     items = response["items"]
        #     for item in items:
        #         item_type = "📁" if item.get("type") == "folder" else "📄"
        #         result += f"{item_type} {item.get('name', 'Unknown')} (ID: {item.get('id', 'N/A')}, Type: {item.get('type', 'N/A')})\n"
        # else:
        #     result += str(response)

        return result
    except Exception as e:
        return f"Error listing folder contents for {folder_id}: {str(e)}"


@tool(parse_docstring=True)
def ask_box_ai_about_loan(folder_id: str, question: str) -> str:
    """Ask Box AI a question about documents in a loan application folder.

    Uses Box AI to analyze documents and answer questions about the loan application.

    Args:
        folder_id: Box folder ID containing the loan application
        question: Question to ask about the loan application

    Returns:
        Box AI's response with information from the documents
    """
    try:
        if conf.box_client is None:
            conf.box_client = get_box_client()
        # First, get all file IDs from the folder
        folder_response = box_folder_items_list(
            client=conf.box_client, folder_id=folder_id, is_recursive=False
        )

        file_ids = []

        for item in folder_response.get("folder_items", []):
            if item.get("type") == "file":
                file_ids.append(item.get("id"))

        # if isinstance(folder_response, dict) and "items" in folder_response:
        #     for item in folder_response["items"]:
        #         if item.get("type") == "file":
        #             file_ids.append(item.get("id"))

        if not file_ids:
            return f"No files found in folder {folder_id}"

        # Ask Box AI about the files
        ai_response = box_ai_ask_file_multi(
            client=conf.box_client, file_ids=file_ids, prompt=question
        )

        # Format the response
        result = f"Box AI Response for: {question}\n\n"

        if isinstance(ai_response, dict):
            ai_response_content = ai_response.get("AI_response", {})
            if "answer" in ai_response_content:
                result += f"Answer: {ai_response_content['answer']}\n\n"
            if "citations" in ai_response_content.get("answer", {}):
                result += "Citations:\n"
                for citation in ai_response_content.get("citations", []):
                    result += f"  - {citation.get('content', 'N/A')}\n"
        else:
            result += str(ai_response)

        return result
    except Exception as e:
        return f"Error asking Box AI about folder {folder_id}: {str(e)}"


@tool(parse_docstring=True)
def extract_structured_loan_data(folder_id: str, fields_schema: str) -> str:
    """Extract structured data from loan application documents using Box AI Extract.

    Args:
        folder_id: Box folder ID containing the loan application
        fields_schema: JSON string defining fields to extract as a list of field definitions, e.g., '[{"type": "string", "key": "applicant_name", "displayName": "Applicant Name"}, {"type": "number", "key": "credit_score", "displayName": "Credit Score"}]'

    Returns:
        Extracted structured data from the documents
    """
    import json

    try:
        if conf.box_client is None:
            conf.box_client = get_box_client()
        # First, get all file IDs from the folder
        folder_response = box_folder_items_list(
            client=conf.box_client, folder_id=folder_id, is_recursive=False
        )

        file_ids = []
        for item in folder_response.get("folder_items", []):
            if item.get("type") == "file":
                file_ids.append(item.get("id"))
        # if isinstance(folder_response, dict) and "items" in folder_response:
        #     for item in folder_response["items"]:
        #         if item.get("type") == "file":
        #             file_ids.append(item.get("id"))
        if not file_ids:
            return f"No files found in folder {folder_id}"

        # Parse the fields schema
        try:
            fields = json.loads(fields_schema)
            if not isinstance(fields, list):
                return f"Error: fields_schema must be a JSON array of field definitions"
        except json.JSONDecodeError as e:
            return f"Error parsing fields_schema: {str(e)}"

        # Extract structured data using Box AI
        ai_response = box_ai_extract_structured_enhanced_using_fields(
            client=conf.box_client, file_ids=file_ids, fields=fields
        )

        # Format the response
        result = f"Extracted Data from Folder {folder_id}:\n\n"
        if isinstance(ai_response, dict):
            result += json.dumps(ai_response, indent=2)
        else:
            result += str(ai_response)

        return result
    except Exception as e:
        return f"Error extracting structured data from folder {folder_id}: {str(e)}"


@tool(parse_docstring=True)
def think_tool(reflection: str) -> str:
    """Tool for strategic reflection on task progress and decision-making.

    Use this tool to analyze your progress, show your work, and plan next steps.
    This creates a deliberate pause in the workflow for quality decision-making.

    When to use:
    - After retrieving data from Box: What key information did I extract?
    - During calculations: Show calculation steps and verify results
    - Before making decisions: Do I have all the data needed?
    - When assessing risk: What factors support my conclusion?

    Args:
        reflection: Your detailed reflection on progress, findings, and next steps

    Returns:
        Confirmation that reflection was recorded
    """
    return f"✓ Reflection recorded: {reflection}"


@tool(parse_docstring=True)
def calculate(expression: str) -> str:
    """Perform mathematical calculations for loan risk analysis.

    Safely evaluates mathematical expressions. Supports basic arithmetic
    operators (+, -, *, /, **, %) and common functions.

    Args:
        expression: Mathematical expression to evaluate (e.g., "(1200 + 380) / 5200")

    Returns:
        Result of the calculation
    """
    import ast
    import operator
    from typing import Any

    # Allowed operations
    operators_map = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
    }

    def eval_expr(node: Any) -> float:
        """Recursively evaluate AST node."""
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            return operators_map[type(node.op)](
                eval_expr(node.left), eval_expr(node.right)
            )
        elif isinstance(node, ast.UnaryOp):
            return operators_map[type(node.op)](eval_expr(node.operand))
        else:
            raise ValueError(f"Unsupported operation: {type(node)}")

    try:
        # Parse and evaluate expression
        tree = ast.parse(expression, mode="eval")
        result = eval_expr(tree.body)

        # Format result nicely
        if isinstance(result, float):
            # Show up to 4 decimal places, remove trailing zeros
            formatted = f"{result:.4f}".rstrip("0").rstrip(".")
            return f"{expression} = {formatted}"
        else:
            return f"{expression} = {result}"
    except Exception as e:
        return f"Error calculating '{expression}': {str(e)}"
