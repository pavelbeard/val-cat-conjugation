from typing import Optional
from pydantic import BaseModel, Field


class AppSettings(BaseModel):
    """
    Application settings schema.
    """

    id: str = Field(default="settings")
    app_name: str = "Val Cat Conjugation"
    version: str = "1.0.0"
    description: str = "A web application for conjugating Catalan verbs."
    show_valencian: bool = Field(
        default=True, description="Show Valencian dialect verbs"
    )
    show_balearic: bool = Field(default=True, description="Show Balearic dialect verbs")
    show_opt_pre2017: bool = Field(
        default=True, description="Show previous valid form until 2017"
    )


class AppSettingsOutput(AppSettings):
    """Output schema for application settings. Without ID field."""
    id: str = Field(default=None, exclude=True)


class AppSettingsUpdate(AppSettings):
    """
    Application settings update schema.
    """
    id: str = Field(default=None, exclude=True)
    
    app_name: Optional[str] = None
    version: Optional[str] = None
    description: Optional[str] = None
    show_valencian: Optional[bool] = None
    show_balearic: Optional[bool] = None
    show_opt_pre2017: Optional[bool] = None
