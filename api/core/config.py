from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

CONSTANTS = {
    "ENV_FILE": ".env",
    "AI_DEFAULT_MODEL": "gpt4o-mini",
}


class Settings(BaseSettings):
    """
    Application settings.
    """

    model_config = SettingsConfigDict(
        env_file=CONSTANTS["ENV_FILE"],
        env_file_encoding="utf-8",
    )

    API_V1_STR: str = Field(
        default="/api/v1",
        description="The API version prefix.",
    )

    # MongoDB connection string
    MONGODB_URL: str = Field(
        default="mongodb://localhost:27017",
        description="The MongoDB connection string.",
        env="MONGODB_URL",
    )
    MONGODB_NAME: str = Field(
        default="verbs",
        description="The name of the MongoDB database.",
        env="MONGODB_NAME",
    )

    # AI API key
    AI_SECRET_KEY: str = Field(default="", description="The AI API key.")

    # AI model to use
    AI_MODEL: str = Field(
        default=CONSTANTS["AI_DEFAULT_MODEL"],
        description="The AI model to use for requests.",
    )


settings = Settings()
