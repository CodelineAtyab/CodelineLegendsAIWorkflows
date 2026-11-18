from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home() -> dict:
    return {"message": "Hello from Docker!"}


@app.get("/health")
def health() -> dict:
    return {"status": "healthy"}