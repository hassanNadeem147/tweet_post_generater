from typing import Literal, TypedDict
from pydantic import BaseModel, Field
class TweetState(TypedDict):
    topic: str
    tweet_generate: str
    reviewer_decision: Literal["approved", "rejected"]
    feedback: str
    iteration: int
    max_iteration: int
    improved_tweet: str
class TweetEvaluation(BaseModel):
    evaluation: Literal["approved", "rejected"] = Field(
        description="Decide whether the generated tweet is ready to publish or needs improvement."
    )

    feedback: str = Field(
        description="Provide specific and actionable feedback explaining what should be improved. If approved, state that no changes are needed."
    )