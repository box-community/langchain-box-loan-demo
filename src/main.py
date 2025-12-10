import logging
from IPython.display import Image, display

from config import config  # noqa: F401 - importing config triggers logging setup
from agents.orchestrator import orchestrator_create
from utils.display_messages import format_messages

logger = logging.getLogger(__name__)


def main() -> None:
    """Main application entry point."""

    orchestrator_agent = orchestrator_create()
    logger.info("Orchestrator agent created successfully")

    # Show the agent
    # display(Image(orchestrator_agent.get_graph().draw_mermaid_png()))

    result = orchestrator_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "research context engineering approaches used to build AI agents",
                }
            ],
        },
    )

    format_messages(result["messages"])


if __name__ == "__main__":
    main()
