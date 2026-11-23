from pydantic import BaseModel, Field, EmailStr, HttpUrl

class EngineerRegistration(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=50
    )
    email: EmailStr
    employee_id: str = Field(
    pattern=r"^ENG-\d{4}$"
)
    age: int = Field(
    ge=18,
    le=65
)
    skills: list[str] = Field(
    min_length=1,
    max_length=5
)
    bio: str | None = Field(
    default=None,
    max_length=200
)
    website: HttpUrl | None = None


def activity_percent(self) -> int:
        return 50

class SoftwareEngineerRegistration(EngineerRegistration):
        def activity_percent(self) -> int:
            return 10
      
class CivilEngineerRegistration(EngineerRegistration):
        def activity_percent(self) -> int:
            return 80
        