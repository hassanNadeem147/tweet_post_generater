from app.graph.state import TweetState, TweetEvaluation
from app.config.settings import config
from app.logging.logger import logger
from langchain_openrouter import ChatOpenRouter


llm_for_generation = ChatOpenRouter(
    api_key=config.OPENROUTER_API_KEY,
    model=config.MODEL_NAME_TWEET_GENERATION,
    temperature=config.TEMPERATURE_TWEET_GENERATION
)

llm_for_review = ChatOpenRouter(
    api_key=config.OPENROUTER_API_KEY,
    model=config.MODEL_NAME_TWEET_REVIEW,
    temperature=config.TEMPERATURE_TWEET_REVIEW
)

llm_for_improvement = ChatOpenRouter(
    api_key=config.OPENROUTER_API_KEY,
    model=config.MODEL_NAME_IMPROVE_TWEET,
    temperature=config.TEMPERATURE_IMPROVE_TWEET
)


async def generate_text(state: TweetState) -> dict:
    logger.info("Tweet generation node started | topic_length={}", len(state["topic"]))
    prompt = f"""
You are a professional social media copywriter.

Your task is to write one professional and engaging tweet about the given topic.

Rules:
- Should be between 150-280 characters.
- Do not exceed 280 characters.
- Plain text only.
- No hashtags.
- No markdown.
- No asterisks.
- No greetings.
- No unnecessary symbols.
- No meaningless or random characters.
- Keep the message clear, concise, attractive, and professional.
- Return only the tweet. Do not provide explanations.

Topic:
{state['topic']}
"""

    try:
        response = await llm_for_generation.ainvoke(prompt)
    except Exception:
        logger.exception("Tweet generation node failed")
        raise

    generated_tweet = response.content.strip()
    logger.info("Tweet generation node completed | characters={}", len(generated_tweet))

    return {
        "tweet_generate": generated_tweet
    }


reviewer_llm = llm_for_review.with_structured_output(TweetEvaluation)


async def review_text(state: TweetState) -> dict:
    logger.info(
        "Tweet review node started | iteration={} | characters={}",
        state["iteration"],
        len(state["tweet_generate"]),
    )
    prompt = f"""
You are a professional Twitter/X content reviewer.

Review the generated tweet and decide whether it is ready to publish.

Topic:
{state['topic']}

Generated Tweet:
{state['tweet_generate']}

Review the tweet based on these requirements:
- Should be between 150-280 characters.
- Clear and easy to understand.
- Concise and engaging.
- Professional and natural.
- Relevant to the given topic.
- Provides meaningful value or insight.
- No unnecessary words or symbols.
- No hashtags.
- No markdown.
- No greetings.
- No grammar or spelling mistakes.
- Should sound human and not generic or AI-generated.

If the tweet satisfies the requirements, approve it.

If the tweet has an important issue that should be fixed, reject it and provide specific, actionable feedback.

Do not rewrite the tweet.
Do not provide a score.
"""

    try:
        response = await reviewer_llm.ainvoke(prompt)
    except Exception:
        logger.exception("Tweet review node failed | iteration={}", state["iteration"])
        raise

    logger.info(
        "Tweet review node completed | decision={} | iteration={}",
        response.evaluation,
        state["iteration"],
    )
    if response.evaluation == "rejected":
        logger.warning(
            "Tweet review rejected generated tweet | iteration={} | feedback={}",
            state["iteration"],
            response.feedback.strip(),
        )

    return {
        "reviewer_decision": response.evaluation,
        "feedback": response.feedback.strip()
    }


async def improve_text(state: TweetState) -> dict:
    logger.info("Tweet improvement node started | iteration={}", state["iteration"])
    prompt = f"""
You are a professional social media copywriter.

Your task is to improve the generated tweet based on the reviewer's feedback.

Topic:
{state['topic']}

Original Tweet:
{state['tweet_generate']}

Reviewer Feedback:
{state['feedback']}

Rules:
- Should be between 150-280 characters.
- Do not exceed 280 characters.
- Keep the tweet relevant to the topic.
- Fix all issues mentioned in the reviewer feedback.
- Make the tweet clear, concise, engaging, and professional.
- Keep the core idea of the original tweet unless the feedback requires changing it.
- Make it sound natural and human.
- No hashtags.
- No markdown.
- No asterisks.
- No greetings.
- No unnecessary symbols.
- Return only the improved tweet.
- Do not provide explanations.
"""

    try:
        response = await llm_for_improvement.ainvoke(prompt)
    except Exception:
        logger.exception("Tweet improvement node failed | iteration={}", state["iteration"])
        raise

    improved_tweet = response.content.strip()
    logger.info(
        "Tweet improvement node completed | iteration={} | characters={}",
        state["iteration"] + 1,
        len(improved_tweet),
    )

    return {
        "tweet_generate": improved_tweet,
        "iteration": state["iteration"] + 1
    }


def reviewer_router(state: TweetState) -> str:
    if state["reviewer_decision"] == "approved":
        logger.info("Tweet workflow approved | iteration={}", state["iteration"])
        return "end"

    if state["iteration"] >= state["max_iteration"]:
        logger.warning(
            "Tweet workflow stopped at maximum iterations | iteration={} | max_iteration={}",
            state["iteration"],
            state["max_iteration"],
        )
        return "end"

    return "improve"