import uvicorn
from random import randint
from quotes import funny_quotes
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi import Request, HTTPException

app = FastAPI()

# http://192.168.100.163/home
@app.get("/home")
async def greetUser() -> HTMLResponse:
    selected_random_quote = funny_quotes[randint(0, len(funny_quotes) - 1)]
    return HTMLResponse(content=f"<html><h1>{selected_random_quote}</h1></html>")

@app.get("/greet")
async def greetUser(user_name: str = "Anonymous") -> dict:
    return {"message": f"Hello {user_name}, welcome to our jokes API!"}

@app.post("/add_quote")
async def add_quote(incoming_request: Request) -> dict:
    json_body = await incoming_request.json()
    new_quote = json_body.get("new_quote")

    funny_quotes.append(new_quote)
    return {"message": f"Quote {new_quote} added successfully!"}

if __name__ == "__main__":
    # Spawn with workers
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
