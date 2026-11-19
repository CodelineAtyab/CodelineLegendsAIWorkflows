from pydantic import BaseModel, EmailStr, Field, HttpUrl


class EngineerRegistration(BaseModel):
    """Registration details shared by every kind of engineer."""

    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    age: int = Field(ge=18, le=65)
    employee_id: str = Field(pattern=r"^ENG-\d{4}$")
    skills: list[str] = Field(min_length=1, max_length=5)
    bio: str | None = Field(default=None, max_length=200)
    website: HttpUrl | None = None

    def activity_percent(self) -> int:
        """Return how active this engineer is, in percent."""
        return 50


class SoftwareEngineerRegistration(EngineerRegistration):
    """Registration for a software engineer."""

    def activity_percent(self) -> int:
        return 10


class CivilEngineerRegistration(EngineerRegistration):
    """Registration for a civil engineer."""

    def activity_percent(self) -> int:
        return 80
