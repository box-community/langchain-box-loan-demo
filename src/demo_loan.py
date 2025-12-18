"""Test script for the loan underwriting orchestrator.

This script demonstrates how to use the loan orchestrator to process
loan applications from Box.
"""

import asyncio
import logging

from agents.loan_orchestrator import loan_orchestrator_create
from utils.display_messages import stream_agent

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def test_loan_application(applicant_name: str):
    """Test the loan orchestrator with a specific applicant.

    Args:
        applicant_name: Name of the loan applicant to process
    """
    logger.info(f"Creating loan orchestrator for applicant: {applicant_name}")

    # Create the orchestrator
    agent = loan_orchestrator_create(applicant_name=applicant_name)

    # Process the loan application
    request = f"Please process the auto loan application for {applicant_name} and provide a complete underwriting decision."

    logger.info(f"Submitting request: {request}")

    # Stream the response
    print("\n" + "=" * 80)
    print(f"PROCESSING LOAN APPLICATION: {applicant_name}")
    print("=" * 80 + "\n")

    await stream_agent(
        agent,
        {
            "messages": [
                {
                    "role": "user",
                    "content": request,
                }
            ]
        },
    )

    print("\n\n" + "=" * 80)
    print("PROCESSING COMPLETE")
    print("=" * 80 + "\n")


async def main():
    """Main test function - run loan processing for all test applicants."""
    # Test applicants covering the full decision spectrum
    test_applicants = [
        "Sarah Chen",  # Expected: AUTO-APPROVE ✅
        "Marcus Johnson",  # Expected: HUMAN REVIEW ⚠️
        "David Martinez",  # Expected: ESCALATION REQUIRED 🚨
        "Jennifer Lopez",  # Expected: AUTO-DENY 🚫
    ]

    print("\n" + "🎯 " * 20)
    print("LOAN UNDERWRITING ORCHESTRATOR - TEST SUITE")
    print("🎯 " * 20 + "\n")

    # Run tests for each applicant
    for i, applicant in enumerate(test_applicants, 1):
        print(f"\n📋 Test {i}/{len(test_applicants)}: {applicant}")
        print("-" * 80)

        try:
            await test_loan_application(applicant)
        except Exception as e:
            logger.error(f"Error processing {applicant}: {str(e)}", exc_info=True)
            print(f"\n❌ ERROR: {str(e)}\n")

        print("\n")

    print("\n" + "✅ " * 20)
    print("ALL TESTS COMPLETE")
    print("✅ " * 20 + "\n")


if __name__ == "__main__":
    # For quick testing, run a single applicant
    # Uncomment one of these lines:

    # asyncio.run(test_loan_application("Sarah Chen"))  # Perfect borrower
    # asyncio.run(test_loan_application("Marcus Johnson"))  # Borderline case
    asyncio.run(test_loan_application("David Martinez"))  # High risk
    asyncio.run(test_loan_application("Jennifer Lopez"))  # Auto-deny

    # Or run all tests:
    # asyncio.run(main())
