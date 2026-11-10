from pydantic import BaseModel, EmailStr, Field, HttpUrl


class EngineerRegistration(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    age: int = Field(ge=18, le=65)
