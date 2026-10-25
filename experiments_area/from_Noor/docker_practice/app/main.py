from fastapi import FastAPI

# FastAPI() creates the web API application.
app = FastAPI()


# @app.get("/") defines the home endpoint.
@app.get("/")
def home():
    return {"message": "Hello from Docker!"}


# @app.get("/health") defines a health-check endpoint.
@app.get("/health")
def health():
    return {"status": "healthy"}
