"""Loan underwriting agent module."""

from agents.loan_underwriting.loan_prompts import (
    BOX_EXTRACT_AGENT_INSTRUCTIONS,
    BOX_UPLOADER_AGENT_INSTRUCTIONS,
    LOAN_ORCHESTRATOR_INSTRUCTIONS,
    POLICY_AGENT_INSTRUCTIONS,
    RISK_CALCULATION_AGENT_INSTRUCTIONS,
)
from agents.loan_underwriting.loan_tools import (
    ask_box_ai_about_loan,
    calculate,
    extract_structured_loan_data,
    list_loan_documents,
    search_loan_folder,
    think_tool,
    upload_text_file_to_box,
)

__all__ = [
    "LOAN_ORCHESTRATOR_INSTRUCTIONS",
    "BOX_EXTRACT_AGENT_INSTRUCTIONS",
    "POLICY_AGENT_INSTRUCTIONS",
    "RISK_CALCULATION_AGENT_INSTRUCTIONS",
    "BOX_UPLOADER_AGENT_INSTRUCTIONS",
    "search_loan_folder",
    "list_loan_documents",
    "ask_box_ai_about_loan",
    "extract_structured_loan_data",
    "think_tool",
    "calculate",
    "upload_text_file_to_box",
]
