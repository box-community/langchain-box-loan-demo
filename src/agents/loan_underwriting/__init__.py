"""Loan underwriting agent module."""

from agents.loan_underwriting.loan_prompts import (
    LOAN_ORCHESTRATOR_INSTRUCTIONS,
    BOX_EXTRACT_AGENT_INSTRUCTIONS,
    POLICY_AGENT_INSTRUCTIONS,
    RISK_CALCULATION_AGENT_INSTRUCTIONS,
)
from agents.loan_underwriting.loan_tools import (
    search_loan_folder,
    list_loan_documents,
    ask_box_ai_about_loan,
    extract_structured_loan_data,
    think_tool,
    calculate,
)

__all__ = [
    "LOAN_ORCHESTRATOR_INSTRUCTIONS",
    "BOX_EXTRACT_AGENT_INSTRUCTIONS",
    "POLICY_AGENT_INSTRUCTIONS",
    "RISK_CALCULATION_AGENT_INSTRUCTIONS",
    "search_loan_folder",
    "list_loan_documents",
    "ask_box_ai_about_loan",
    "extract_structured_loan_data",
    "think_tool",
    "calculate",
]
