
"""Pydantic models for engineer registration."""

from pydantic import BaseModel, EmailStr, Field, HttpUrl


class EngineerRegistration(BaseModel):
    """Validate common engineer registration fields."""

    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    age: int = Field(ge=18, le=65)
    employee_id: str = Field(pattern=r"^ENG-[0-9]{4}$")
    skills: list[str] = Field(min_length=1, max_length=5)
    bio: str | None = Field(default=None, max_length=200)
    website: HttpUrl | None = None

    def activity_percent(self) -> int:
        """Return the default engineer activity percentage."""
        return 50


class SoftwareEngineerRegistration(EngineerRegistration):
    """Registration model for software engineers."""

    def activity_percent(self) -> int:
        """Return the software engineer activity percentage."""
        return 10


class CivilEngineerRegistration(EngineerRegistration):
    """Registration model for civil engineers."""

    def activity_percent(self) -> int:
        """Return the civil engineer activity percentage."""
        return 80
