# Engineer Registration API

A REST API built with **FastAPI** and **Pydantic** to demonstrate request validation, model inheritance, and method overriding through Software Engineer and Civil Engineer registration.

## Features

- Engineer registration using Pydantic models.
- Automatic request data validation.
- Parent and child model inheritance.
- Method overriding for engineer activity percentages.
- Interactive API documentation using Swagger UI.

## Project Structure

```text
engineer_registration/
│
├── models/
│   ├── __init__.py
│   └── engineer.py
│
├── main.py
├── pyproject.toml
├── uv.lock
├── .python-version
└── README.md
```

## Engineer Model Validation

The parent `EngineerRegistration` model defines the common fields inherited by both engineer types.

| Field | Type | Validation |
|---|---|---|
| name | str | Required, 2–50 characters |
| email | EmailStr | Required, valid email |
| age | int | Required, 18–65 |
| employee_id | str | Required, format: ENG-#### |
| skills | list[str] | Required, 1–5 items |
| bio | str or None | Optional, maximum 200 characters |
| website | HttpUrl or None | Optional, valid HTTP/HTTPS URL |

## Model Inheritance

Two child models inherit from `EngineerRegistration`:

- **SoftwareEngineerRegistration:** Overrides `activity_percent()` to return `10`.
- **CivilEngineerRegistration:** Overrides `activity_percent()` to return `80`.

The parent model returns `50` by default.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/engineers/software` | Register a Software Engineer |
| POST | `/engineers/civil` | Register a Civil Engineer |

### Example Request

```json
{
  "name": "Noor Alhuda",
  "email": "noor@example.com",
  "age": 25,
  "employee_id": "ENG-1234",
  "skills": ["Python", "FastAPI", "Cybersecurity"],
  "bio": "Software engineer",
  "website": "https://example.com"
}
```

### Example Response

```json
{
  "name": "Noor Alhuda",
  "email": "noor@example.com",
  "activity_percent": 10
}
```

## Installation and Setup

### Prerequisites

- Python 3.14 or later
- [uv](https://docs.astral.sh/uv/)

### 1. Install Dependencies

From the project directory, run:

```bash
uv sync
```

### 2. Run the Application

```bash
uv run uvicorn main:app --reload --port 8080
```

The API will be available at:

```text
http://localhost:8080
```

## API Documentation

FastAPI automatically generates interactive Swagger documentation.

Open:

```text
http://localhost:8080/docs
```

Use Swagger UI to submit registration requests and test the validation rules.

## Validation Responses

- **200 OK:** Registration successful.
- **422 Unprocessable Content:** Request data failed validation.

## Code Quality

Ruff is used for Python formatting and linting.

Run the following commands:

```bash
uv run ruff format .
uv run ruff check .
```

## Technologies Used

- Python 3.14
- FastAPI
- Pydantic
- Uvicorn
- uv
- Ruff
