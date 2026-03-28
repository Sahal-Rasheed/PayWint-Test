from fastapi import FastAPI
from fastapi.responses import JSONResponse

from handler import expense_router
from db import create_db_and_tables


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def root():
    return JSONResponse({"message": "index"})


app.include_router(expense_router)
