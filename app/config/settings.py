from pydantic_settings import BaseSettings,SettingsConfigDict
class SettingModel(BaseSettings):
    """Configuration for secrets"""
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8"
    )
    OPENROUTER_API_KEY: str
    MODEL_NAME_TWEET_GENERATION: str
    TEMPERATURE_TWEET_GENERATION: float
    MODEL_NAME_TWEET_REVIEW: str
    TEMPERATURE_TWEET_REVIEW: float
    MODEL_NAME_IMPROVE_TWEET: str
    TEMPERATURE_IMPROVE_TWEET: float
config = SettingModel()