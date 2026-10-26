from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home() -> dict:
    """Return the required welcome message."""
    return {"message": "Hello from Docker!"}


@app.get("/health")
def health() -> dict:
    """Return the required application status."""
    return {"status": "healthy"}