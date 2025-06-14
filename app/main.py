from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import recipe_table
from app.database.database import database, metadata, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    metadata.create_all(engine)
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/recipes")
async def get_recipes():
    query = "SELECT * FROM recipes"
    rows = await database.fetch_all(query=query)
    return rows