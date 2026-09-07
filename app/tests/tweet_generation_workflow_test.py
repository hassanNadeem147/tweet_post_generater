from app.graph.workflow import app
from app.logging.logger import logger
import asyncio
initial_stage = {
    "topic": "The future of AI in healthcare",
    "tweet_generate": "",
    "reviewer_decision": "",
    "feedback": "",
    "iteration": 0,
    "max_iteration": 5,
    "improved_tweet": ""
}
async def main():
    workflow_result = await app.ainvoke(initial_stage)

    logger.info(f"Workflow result: {workflow_result}")


asyncio.run(main())