"""Stretch exploration: turning models into dict/JSON and back, plus lax vs strict mode.

Run with: uv run explore_serialization.py
"""

from pydantic import ValidationError

from models.engineer import SoftwareEngineerRegistration

raw = {
    "name": "Mona Al Said",
    "email": "mona@example.com",
    "age": 27,
    "employee_id": "ENG-0042",
    "skills": ["python", "fastapi"],
    "website": "https://mona.dev",
}

# dict -> model (deserialization)
engineer = SoftwareEngineerRegistration.model_validate(raw)
print("model_validate      ->", repr(engineer))

# model -> dict (serialization to Python types; website stays an HttpUrl object)
print("model_dump          ->", engineer.model_dump())

# model -> dict with JSON-friendly types only (website becomes a plain str)
print("model_dump(json)    ->", engineer.model_dump(mode="json"))

# model -> JSON text
as_json = engineer.model_dump_json()
print("model_dump_json     ->", as_json)

# JSON text -> model
back = SoftwareEngineerRegistration.model_validate_json(as_json)
print("model_validate_json ->", back == engineer)

# Leave out the optional fields that were never sent
print("exclude_unset       ->", engineer.model_dump(mode="json", exclude_unset=True))

# Lax (default) vs strict mode when age arrives as text
text_age = {**raw, "age": "27"}
lax = SoftwareEngineerRegistration.model_validate(text_age)
print("lax   age='27'      ->", lax.age, type(lax.age).__name__)
try:
    SoftwareEngineerRegistration.model_validate(text_age, strict=True)
except ValidationError as error:
    print("strict age='27'     ->", error.errors()[0]["msg"])
