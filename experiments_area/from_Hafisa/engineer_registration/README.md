# Engineer registration API

Implements issue #277 with a shared Pydantic registration model and software/civil subclasses.

## Run

From this directory, run `uv run main.py` with Python 3.14.
Open http://localhost:8080/docs to try `POST /engineers/software` and `POST /engineers/civil`.
This is a no-package uv project in the parent workspace; dependencies are locked in `../uv.lock`.

## Example
