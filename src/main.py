import asyncio
import logging

from agents.orchestrator import orchestrator_create
from app_config import conf  # noqa: F401 - importing config triggers logging setup
from utils.display_messages import stream_agent

logger = logging.getLogger(__name__)


async def main() -> None:
    """Main application entry point."""

    orchestrator_agent = orchestrator_create()
    logger.info("Orchestrator agent created successfully")

    # Show the agent
    # display(Image(orchestrator_agent.get_graph().draw_mermaid_png()))

    # result = orchestrator_agent.invoke(
    #     {
    #         "messages": [
    #             {
    #                 "role": "user",
    #                 "content": "research context engineering approaches used to build AI agents",
    #             }
    #         ],
    #     },
    # )

    # format_messages(result["messages"])

    await stream_agent(
        orchestrator_agent,
        {
            "messages": [
                {
                    "role": "user",
                    "content": "research context engineering approaches used to build AI agents",
                }
            ]
        },
    )


if __name__ == "__main__":
    asyncio.run(main())
