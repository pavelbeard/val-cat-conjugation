from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.constants import CONSTANTS


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

    # MongoDB credentials
    MONGODB_USER: str = Field(
        default="admin",
        description="The MongoDB username.",
        env="MONGODB_USER",
    )
    MONGODB_PASSWORD: str = Field(
        default="admin",
        description="The MongoDB password.",
        env="MONGODB_PASSWORD",
    )

    # MongoDB connection URL and database name
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

    # AI API keys
    # GENERAL AI API key for OpenAI, Ollama, etc.
    AI_SECRET_KEY: str = Field(
        default="", description="The AI API key.", env="AI_SECRET_KEY"
    )

    OPENAI_API_KEY: str = Field(
        default="", description="The OpenAI API key.", env="OPENAI_API_KEY"
    )

    OLLAMA_API_KEY: str = Field(
        default="", description="The Ollama API key.", env="OLLAMA_API_KEY"
    )

    GEMINI_API_KEY: str = Field(
        default="", description="The Gemini API key.", env="GEMINI_API_KEY"
    )

    # AI models
    # GENERAL AI model to use for requests
    AI_MODEL: str = Field(
        default=CONSTANTS["AI_DEFAULT_MODEL"],
        description="The AI model to use for requests.",
    )

    OPENAI_MODEL: str = Field(
        default="gpt-4o-mini",
        description="The OpenAI model to use for requests.",
        env="OPENAI_MODEL",
    )

    OLLAMA_MODEL: str = Field(
        default="llama3",
        description="The Ollama model to use for requests.",
        env="OLLAMA_MODEL",
    )

    GEMINI_MODEL: str = Field(
        default="gemini-2.5-flash",
        description="The Gemini model to use for requests.",
        env="GEMINI_MODEL",
    )


class TestSettings(Settings):
    """
    Settings for testing environment.
    """

    model_config = SettingsConfigDict(
        env_file=".env.test",
        env_file_encoding="utf-8",
    )


settings = Settings()
test_settings = TestSettings()
