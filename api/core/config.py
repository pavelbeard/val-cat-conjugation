from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

CONSTANTS = {
    "ENV_FILE": ".env",
    "OPENAI_DEFAULT_MODEL": "gpt-3.5-turbo",
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

    # OpenAI API key
    OPENAI_API_KEY: str = Field(default="", description="The OpenAI API key.")

    # OpenAI model to use
    OPENAI_MODEL: str = Field(
        default=CONSTANTS["OPENAI_DEFAULT_MODEL"],
        description="The OpenAI model to use for requests.",
    )


settings = Settings()
