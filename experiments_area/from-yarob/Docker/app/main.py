from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello from codeline world!"}

@app.get("/health")
def health():
    return {"status": "healthy"}
