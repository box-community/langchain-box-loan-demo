"""
Loan Underwriting Orchestrator Agent.

This module implements the main orchestrator agent using LangChain's Deep Agents framework.
The orchestrator coordinates the complete loan underwriting workflow with:
- Persistent filesystem-based memory across sessions
- Integration with Box API for document retrieval
- Multi-step loan decisioning workflow
- Violation tracking and approval authority routing
"""

import logging
import os
from pathlib import Path
from typing import Any

from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, FilesystemBackend, StateBackend
from langchain_anthropic import ChatAnthropic
from langgraph.checkpoint.memory import MemorySaver

logger = logging.getLogger(__name__)

# Default memory directory for persistent storage
DEFAULT_MEMORY_DIR = Path.home() / ".langchain-box-loan-demo" / "memories"


class LoanUnderwritingOrchestrator:
    """
    Main orchestrator agent for loan underwriting workflow.

    This agent coordinates the complete loan underwriting process:
    1. Document retrieval from Box
    2. Data extraction and validation
    3. Risk assessment and violation detection
    4. Decision routing based on approval authority
    5. Result documentation and reporting

    Features:
    - Persistent memory across sessions (stored in filesystem)
    - Planning and task decomposition
    - Access to Box API tools for document operations
    - Violation-based decisioning framework
    """

    def __init__(
        self,
        model: str = "claude-sonnet-4-5-20250929",
        memory_dir: str | Path | None = None,
        api_key: str | None = None,
    ):
        """
        Initialize the loan underwriting orchestrator.

        Args:
            model: Anthropic model to use (default: Claude Sonnet 4.5)
            memory_dir: Directory for persistent memory storage
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        """
        self.model_name = model
        self.memory_dir = Path(memory_dir) if memory_dir else DEFAULT_MEMORY_DIR
        self.memory_dir.mkdir(parents=True, exist_ok=True)

        # Initialize Anthropic model
        self.llm = ChatAnthropic(
            model=self.model_name,
            api_key=api_key or os.getenv("ANTHROPIC_API_KEY"),
            temperature=0,  # Deterministic for financial decisioning
        )

        # System prompt for loan underwriting
        self.system_prompt = self._build_system_prompt()

        # Initialize the deep agent
        self.agent = self._create_agent()

        logger.info(
            f"Initialized LoanUnderwritingOrchestrator with model={model}, "
            f"memory_dir={self.memory_dir}"
        )

    def _build_system_prompt(self) -> str:
        """Build the system prompt for the loan underwriting orchestrator."""
        return """You are an expert loan underwriting orchestrator agent.

Your role is to coordinate the complete auto loan underwriting workflow:

## Core Responsibilities

1. **Document Processing**
   - Retrieve loan application documents from Box
   - Extract key data points (income, credit, DTI, LTV)
   - Validate data completeness and accuracy

2. **Risk Assessment**
   - Calculate debt-to-income (DTI) ratio
   - Evaluate credit worthiness
   - Assess loan-to-value (LTV) ratio
   - Identify policy violations

3. **Violation Framework**
   Track violations by severity:
   - **Minor**: Single threshold breach within tolerance (DTI 43-45%, credit 610-619)
   - **Moderate**: Larger breach or combination (DTI 45-48%, credit 600-609)
   - **Major**: Severe breach (DTI >48%, credit <600, recent repo, 3+ collections)

4. **Decision Routing**
   - **Auto-Approve**: Zero violations, all criteria met
   - **Human Review**: 1-2 minor violations (→ Senior Underwriter)
   - **Escalation**: Moderate or multiple violations (→ Regional Director)
   - **Auto-Deny**: Major violations or 3+ violations total

## Key Metrics

- **DTI Threshold**: 43% max (warning at 40%)
- **Credit Score**: 620 minimum
- **LTV**: Varies by vehicle age (90-120%)
- **Employment**: 2 years minimum
- **Collections**: $5,000 max
- **Repossession**: None in 36 months

## Workflow Steps

1. Read underwriting policies from /memories/policies/
2. Retrieve application documents from Box
3. Extract and validate applicant data
4. Calculate risk metrics (DTI, LTV, etc.)
5. Identify and classify violations
6. Route to appropriate decision authority
7. Document decision rationale
8. Save decision summary to /memories/decisions/

## Memory Management

- Store underwriting policies in /memories/policies/ (persistent)
- Store completed decisions in /memories/decisions/ (persistent)
- Use working files for temporary analysis (ephemeral)
- Learn from patterns across applications

## Important Notes

- Always be thorough and conservative with risk assessment
- Document all violation findings clearly
- Consider compensating factors (large down payment, reserves, co-signer)
- Maintain complete audit trail for compliance
- Use precise calculations - financial accuracy is critical
"""

    def _create_agent(self) -> Any:
        """
        Create the deep agent with persistent filesystem memory.

        Uses CompositeBackend to route:
        - /memories/* → FilesystemBackend (persistent across sessions)
        - Other paths → StateBackend (ephemeral, per-thread)
        """
        # Create filesystem backend for persistent memory
        filesystem_backend = FilesystemBackend(
            root_dir=str(self.memory_dir),
            virtual_mode=False,  # Use real filesystem
        )

        # Create composite backend factory
        def create_backend(runtime):
            """Factory function to create composite backend with routing."""
            return CompositeBackend(
                default=StateBackend(runtime),
                routes={
                    "/memories/": filesystem_backend,
                }
            )

        # Create deep agent with custom backend
        agent = create_deep_agent(
            model=self.llm,
            backend=create_backend,
            system_prompt=self.system_prompt,
            tools=[],  # TODO: Add Box API tools here
            checkpointer=MemorySaver(),  # In-memory checkpointing for now
        )

        return agent

    def process_loan_application(
        self,
        applicant_name: str,
        thread_id: str | None = None,
    ) -> dict[str, Any]:
        """
        Process a loan application through the complete underwriting workflow.

        Args:
            applicant_name: Name of the loan applicant
            thread_id: Optional thread ID for conversation continuity

        Returns:
            dict containing the underwriting decision and details
        """
        logger.info(f"Processing loan application for: {applicant_name}")

        # Create configuration with thread_id
        config = {
            "configurable": {
                "thread_id": thread_id or f"loan_{applicant_name.lower().replace(' ', '_')}"
            }
        }

        # Initial prompt to the agent
        prompt = f"""Process the loan application for {applicant_name}.

Please follow the complete underwriting workflow:
1. Check /memories/policies/ for underwriting standards
2. Retrieve applicant documents from Box
3. Extract and validate all required data
4. Calculate DTI, LTV, and other risk metrics
5. Identify any policy violations
6. Make recommendation based on violation framework
7. Save decision summary to /memories/decisions/{applicant_name.lower().replace(' ', '_')}.md

Provide a complete analysis with clear reasoning for the decision."""

        try:
            # Invoke the agent
            result = self.agent.invoke(
                {"messages": [{"role": "user", "content": prompt}]},
                config=config
            )

            logger.info(f"Successfully processed application for {applicant_name}")
            return result

        except Exception as e:
            logger.error(f"Error processing loan application: {e}", exc_info=True)
            raise

    def initialize_policies(self) -> None:
        """
        Initialize the agent's memory with underwriting policies.

        Loads policy documents and stores them in /memories/policies/
        for persistent access across all loan processing sessions.
        """
        logger.info("Initializing underwriting policies in agent memory")

        config = {"configurable": {"thread_id": "policy_initialization"}}

        prompt = """Initialize the underwriting policy memory.

Please read the underwriting policy documents from the data/Policies/ directory
and save them to /memories/policies/ for persistent access:

1. Read data/Policies/Auto Loan Underwriting Standards.md
2. Read data/Policies/Exception Approval Authority.md
3. Read data/Policies/Vehicle Valuation Guidelines.md
4. Save summaries to /memories/policies/underwriting_standards.md
5. Save key decision thresholds for quick reference

This will ensure all future loan processing uses consistent policy standards."""

        try:
            self.agent.invoke(
                {"messages": [{"role": "user", "content": prompt}]},
                config=config
            )
            logger.info("Successfully initialized underwriting policies")
        except Exception as e:
            logger.error(f"Error initializing policies: {e}", exc_info=True)
            raise

    def get_memory_status(self) -> dict[str, Any]:
        """
        Get status of the persistent memory filesystem.

        Returns:
            dict with memory statistics and stored files
        """
        policies_dir = self.memory_dir / "policies"
        decisions_dir = self.memory_dir / "decisions"

        status = {
            "memory_dir": str(self.memory_dir),
            "exists": self.memory_dir.exists(),
            "policies": {
                "dir": str(policies_dir),
                "exists": policies_dir.exists(),
                "files": list(policies_dir.glob("*.md")) if policies_dir.exists() else [],
            },
            "decisions": {
                "dir": str(decisions_dir),
                "exists": decisions_dir.exists(),
                "files": list(decisions_dir.glob("*.md")) if decisions_dir.exists() else [],
            }
        }

        return status


def create_orchestrator(
    memory_dir: str | Path | None = None,
    api_key: str | None = None,
) -> LoanUnderwritingOrchestrator:
    """
    Factory function to create a loan underwriting orchestrator agent.

    Args:
        memory_dir: Directory for persistent memory storage
        api_key: Anthropic API key

    Returns:
        Configured LoanUnderwritingOrchestrator instance
    """
    return LoanUnderwritingOrchestrator(
        memory_dir=memory_dir,
        api_key=api_key,
    )
