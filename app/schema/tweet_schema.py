from pydantic import BaseModel, Field
class TweetGenerationRequest(BaseModel):
    topic: str = Field(
        ...,
        description="The topic or subject for which the tweet should be generated."
    )
class TweetGenerationResponse(BaseModel):
    tweet: str = Field(
        ...,
        description="The generated tweet based on the provided topic."
    )