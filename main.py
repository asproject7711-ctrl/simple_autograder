# main.py
from fastapi import FastAPI
from routers import token_routes, autograder_routes

app = FastAPI(title="Edu Platform (No-SQL) – Token Tracking & Autograder")

app.include_router(token_routes.router)
app.include_router(autograder_routes.router)

@app.get("/")
def root():
    return {"message": "Token tracking & autograder is up ✨"}
