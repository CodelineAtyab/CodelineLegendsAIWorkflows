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
