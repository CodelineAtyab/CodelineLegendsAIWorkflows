from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def home() -> dict:
    return {"message": "Hello from Docker!"}


@app.get("/health")
async def health() -> dict:
    return {"status": "healthy"}
