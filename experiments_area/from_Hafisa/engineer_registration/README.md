# Engineer registration API

Implements issue #277 with a shared Pydantic registration model and software/civil subclasses.

## Run

From this directory, run `uv run main.py` with Python 3.14.
Open http://localhost:8080/docs to try `POST /engineers/software` and `POST /engineers/civil`.
This is a no-package uv project in the parent workspace; dependencies are locked in `../uv.lock`.

## Example

Send `{"name":"Mona Al Said","email":"mona@example.com","age":27,"employee_id":"ENG-0042","skills":["python","fastapi"]}` to either route.
The software response is `{"name":"Mona Al Said","email":"mona@example.com","activity_percent":10}`.
The civil route returns the same fields with `activity_percent` equal to 80; the parent method returns 50.
Rules for all seven fields live in the parent model, and FastAPI validates the typed request body.

## Verification (2026-11-10)

All 36 HTTP checks passed using FastAPI TestClient against the actual app.
Both routes returned 200 with exactly the three expected fields for the valid example.
Both returned 422 naming the failing field for all 11 issue examples: invalid email, short/long name, age 17, nonnumeric age, malformed ID, empty/oversized skills, long bio, invalid website, and missing email.
Both accepted inclusive name/age/list/bio boundaries and optional nulls; both rejected age 66 and IDs with a prefix, suffix, or trailing newline.
The parent activity method returned 50; Swagger and OpenAPI exposed both routes.
`uv run --frozen main.py` started successfully and served OpenAPI on port 8080.
Ruff 0.16.10 and mypy 2.4.0 were used for lint and type checks.
Validation requests were executed programmatically; Swagger was available, but manual Swagger submissions were not performed.

## Strictness exploration

Pydantic's default lax mode converts an age supplied as `"27"` into the integer 27.
Calling `EngineerRegistration.model_validate(payload, strict=True)` rejects that text age; both behaviors were checked.
The API keeps the default lax behavior required by this exercise.
Reference: https://docs.pydantic.dev/latest/concepts/strict_mode/
