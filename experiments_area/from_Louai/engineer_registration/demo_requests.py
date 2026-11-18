"""Send the valid example and every invalid example from issue #277 to the running API.

Start the server first (uv run main.py), then in a second terminal:
    uv run demo_requests.py
Use another address with the BASE_URL environment variable, for example:
    BASE_URL=http://192.168.1.10:8080 uv run demo_requests.py
"""

import json
import os
import urllib.error
import urllib.request

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8080")

VALID = {
    "name": "Mona Al Said",
    "email": "mona@example.com",
    "age": 27,
    "employee_id": "ENG-0042",
    "skills": ["python", "fastapi"],
}

INVALID_CHANGES = {
    'email "mona-at-example"': {"email": "mona-at-example"},
    'name "M"': {"name": "M"},
    "name with 51 characters": {"name": "x" * 51},
    "age 17": {"age": 17},
    'age "twenty"': {"age": "twenty"},
    'employee_id "ENG-42"': {"employee_id": "ENG-42"},
    "skills []": {"skills": []},
    "skills with 6 items": {"skills": ["a", "b", "c", "d", "e", "f"]},
    "bio with 201 characters": {"bio": "x" * 201},
    'website "not a url"': {"website": "not a url"},
}


def post(path: str, body: dict) -> tuple[int, dict]:
    request = urllib.request.Request(
        BASE_URL + path,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request) as response:
            return response.status, json.loads(response.read())
    except urllib.error.HTTPError as error:
        return error.code, json.loads(error.read())


def show_error(label: str, status: int, body: dict) -> None:
    detail = body.get("detail")
    if not isinstance(detail, list):
        print(f"{status}  {label:26} unexpected response: {body}")
        return
    first = detail[0]
    field = first["loc"][-1]
    print(f"{status}  {label:26} field={field:12} {first['msg']}")


def main() -> None:
    print(f"Target: {BASE_URL}\n")
    print("Valid requests")
    for path in ("/engineers/software", "/engineers/civil"):
        status, body = post(path, VALID)
        print(f"{status}  {path:26} {body}")

    print("\nInvalid requests (POST /engineers/software)")
    for label, change in INVALID_CHANGES.items():
        status, body = post("/engineers/software", {**VALID, **change})
        show_error(label, status, body)

    without_email = {key: value for key, value in VALID.items() if key != "email"}
    status, body = post("/engineers/software", without_email)
    show_error("email removed", status, body)


if __name__ == "__main__":
    main()
