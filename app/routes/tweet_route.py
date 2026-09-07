from fastapi import APIRouter, HTTPException
from openrouter.errors import TooManyRequestsResponseError

from app.graph.workflow import app
from app.schema.tweet_schema import (
    TweetGenerationRequest,
    TweetGenerationResponse
)
from app.logging.logger import logger


router = APIRouter()


@router.post(
    "/generate_tweet",
    response_model=TweetGenerationResponse
)
async def generate_tweet(request: TweetGenerationRequest):

    logger.info(
        f"Tweet generation started | topic={request.topic}"
    )

    initial_state = {
        "topic": request.topic,
        "tweet_generate": "",
        "reviewer_decision": "",
        "feedback": "",
        "iteration": 0,
        "max_iteration": 5,
        "improved_tweet": ""
    }

    try:

        workflow_result = await app.ainvoke(initial_state)

        generated_tweet = workflow_result.get(
            "tweet_generate",
            ""
        )

        decision = workflow_result.get(
            "reviewer_decision"
        )

        iteration = workflow_result.get(
            "iteration"
        )

        # Normal successful completion
        if decision == "approved":

            logger.info(
                f"Tweet generation completed | "
                f"decision={decision} | "
                f"iteration={iteration}"
            )

        # Maximum iterations reached
        else:

            logger.warning(
                f"Tweet generation reached max iterations | "
                f"decision={decision} | "
                f"iteration={iteration}"
            )

        return TweetGenerationResponse(
            tweet=generated_tweet
        )

    except TooManyRequestsResponseError as error:
        logger.warning(
            "OpenRouter rate limit exceeded | topic_length={} | provider_error={}",
            len(request.topic),
            str(error),
        )
        raise HTTPException(
            status_code=429,
            detail="The AI provider rate limit has been reached. Please try again later or add credits to your OpenRouter account.",
        ) from error

    except Exception:

        logger.exception(
            f"Tweet generation failed | topic={request.topic}"
        )

        raise