# Engineer Registration API

Practice project for issue #277: a FastAPI app that registers engineers and lets
Pydantic reject bad input with `422` before the route function runs.

## Run

```bash
uv run main.py
```

The server listens on port **8080**. Swagger UI: <http://localhost:8080/docs>

> If something else on your machine already uses port 8080 (for example a Docker
> container), `localhost:8080` reaches that program instead. Stop it first, or open
> the docs through your machine's network address, e.g. `http://192.168.x.x:8080/docs`.

## Routes

| Method | Path | Body | Response |
|---|---|---|---|
| `POST` | `/engineers/software` | `SoftwareEngineerRegistration` | `name`, `email`, `activity_percent` (10) |
| `POST` | `/engineers/civil` | `CivilEngineerRegistration` | `name`, `email`, `activity_percent` (80) |

## Validation rules (`models/engineer.py`)

| Field | Type | Rule |
|---|---|---|
| `name` | `str` | 2 to 50 characters |
| `email` | `EmailStr` | valid email |
| `age` | `int` | 18 to 65 inclusive |
| `employee_id` | `str` | `^ENG-\d{4}$`, e.g. `ENG-0042` |
| `skills` | `list[str]` | 1 to 5 items |
| `bio` | `str \| None` | optional, at most 200 characters |
| `website` | `HttpUrl \| None` | optional, valid URL |

`EngineerRegistration.activity_percent()` returns `50`; the software and civil
children override it with `10` and `80`.

## Try it

With the server running, send the valid example and every invalid example from the issue:

```bash
uv run demo_requests.py
```

Set `BASE_URL` to target another address (default `http://localhost:8080`).

## Stretch: serialization and strict mode

```bash
uv run explore_serialization.py
```

Shows `model_validate`, `model_dump`, `model_dump(mode="json")`, `model_dump_json`,
`model_validate_json`, `exclude_unset`, and lax vs strict mode for `"age": "27"`.
