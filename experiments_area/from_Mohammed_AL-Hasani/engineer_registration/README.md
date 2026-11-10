# Engineer Registration API

FastAPI app that registers engineers and validates input with Pydantic.

## Run

```
uv run main.py
```

Server: http://localhost:8080 — Swagger UI: http://localhost:8080/docs

## Routes

- `POST /engineers/software` — returns `name`, `email`, `activity_percent` (10)
- `POST /engineers/civil` — returns `name`, `email`, `activity_percent` (80)

All validation rules live in `models/engineer_model.py`. Invalid input gets `422`.
