from fastapi import FastAPI
from app.routes.tweet_route import router as tweet_router
from app.logging.logger import logger

app = FastAPI(title="Tweet Generation API", description="API for generating tweets based on a given topic.", version="1.0.0")


@app.get("/")
async def root():
    logger.info("Health check requested")
    return {"message": "Welcome to the Tweet Generation API. Use the /api/generate_tweet endpoint to generate tweets based on a topic."}


# Include the tweet generation router
app.include_router(tweet_router, prefix="/api", tags=["Tweet Generation"])