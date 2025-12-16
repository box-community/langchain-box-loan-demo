"""Loan Underwriting Orchestrator - Deep Agent for loan processing.

This module creates a deep underwriting agent that coordinates specialized sub-agents
to process auto loan applications and make risk-based decisions.
"""

from datetime import datetime
from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, FilesystemBackend, StateBackend
from langchain.chat_models import init_chat_model
from langgraph.graph.state import CompiledStateGraph

from agents.loan_underwriting import (
    BOX_EXTRACT_AGENT_INSTRUCTIONS,
    LOAN_ORCHESTRATOR_INSTRUCTIONS,
    POLICY_AGENT_INSTRUCTIONS,
    RISK_CALCULATION_AGENT_INSTRUCTIONS,
    ask_box_ai_about_loan,
    calculate,
    extract_structured_loan_data,
    list_loan_documents,
    search_loan_folder,
    think_tool,
    upload_text_file_to_box,
)
from app_config import conf


def loan_orchestrator_create(applicant_name: str) -> CompiledStateGraph:
    """Create the loan underwriting orchestrator agent.

    Returns:
        CompiledStateGraph: The configured deep agent for loan underwriting
    """
    # Get current date for context
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Define sub-agents for loan processing workflow

    # Sub-agent 1: Document Extraction & Box Integration
    box_extract_agent = {
        "name": "box-extract-agent",
        "description": (
            "Specialist for retrieving and extracting data from loan application documents in Box. "
            "Use this agent to locate folders, list documents, and extract structured data from loan files."
            "A box_upload_cache.json file exists in the memories folder with the location of all demo files in box."
        ),
        "system_prompt": BOX_EXTRACT_AGENT_INSTRUCTIONS.format(
            date=current_date, applicant_name=applicant_name
        ),
        "tools": [
            search_loan_folder,
            list_loan_documents,
            ask_box_ai_about_loan,
            extract_structured_loan_data,
            think_tool,
            # upload_text_file_to_box,
        ],
    }

    # Sub-agent 2: Policy Interpretation
    policy_agent = {
        "name": "policy-agent",
        "description": (
            "Specialist for interpreting underwriting policies and rules. "
            "Use this agent to query policy thresholds, approval authority levels, and compliance rules."
            "A box_upload_cache.json file exists in the memories folder with the location of all demo files in box."
        ),
        "system_prompt": POLICY_AGENT_INSTRUCTIONS.format(
            date=current_date, applicant_name=applicant_name
        ),
        "tools": [
            ask_box_ai_about_loan,  # Can query policy documents in Box
            think_tool,
            # upload_text_file_to_box,
        ],
    }

    # Sub-agent 3: Risk Calculation & Analysis
    risk_calculation_agent = {
        "name": "risk-calculation-agent",
        "description": (
            "Specialist for quantitative risk analysis. "
            "Use this agent to calculate DTI, LTV, identify policy violations, and assess risk levels."
            "A box_upload_cache.json file exists in the memories folder with the location of all demo files in box."
        ),
        "system_prompt": RISK_CALCULATION_AGENT_INSTRUCTIONS.format(
            date=current_date, applicant_name=applicant_name
        ),
        "tools": [
            calculate,
            think_tool,
            # upload_text_file_to_box,
        ],
    }

    # Sub-agent 4: Box Uploader for saving reports and data
    # box_uploader_agent = {
    #     "name": "box-uploader-agent",
    #     "description": (
    #         "Specialist for uploading documents to Box. "
    #         "Use this agent to upload underwriting reports and save application data to Box."
    #         "A box_upload_cache.json file exists in the memories folder with the location of all demo files in box."
    #     ),
    #     "system_prompt": BOX_UPLOADER_AGENT_INSTRUCTIONS.format(
    #         date=current_date, applicant_name=applicant_name
    #     ),
    #     "tools": [
    #         upload_text_file_to_box,
    #         think_tool,
    #     ],
    # }

    # Create the main LLM model
    model = init_chat_model(
        model="anthropic:claude-sonnet-4-5-20250929",
        temperature=0.0,
        api_key=conf.ANTHROPIC_API_KEY,
    )

    # Configure backend for persistent memory
    memories_folder = Path(__file__).parent.parent.parent / "agents_memories"
    memories_folder.mkdir(parents=True, exist_ok=True)

    # Create filesystem backend for persistent memory
    filesystem_backend = FilesystemBackend(
        root_dir=str(memories_folder),
        virtual_mode=True,
    )

    # Create composite backend factory
    def backend(rt):
        return CompositeBackend(
            default=StateBackend(rt),
            routes={
                "/memories/": filesystem_backend,
            },
        )

    # Create the orchestrator agent
    agent = create_deep_agent(
        model=model,
        tools=[upload_text_file_to_box],
        system_prompt=LOAN_ORCHESTRATOR_INSTRUCTIONS.format(
            date=current_date, applicant_name=applicant_name
        ),
        subagents=[
            box_extract_agent,
            policy_agent,
            risk_calculation_agent,
            # box_uploader_agent,
        ],  # type: ignore
        backend=backend,  # type: ignore
    )

    return agent
