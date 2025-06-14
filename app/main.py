from typing import Optional
from fastapi import Depends, FastAPI
from contextlib import asynccontextmanager
from app.database import recipe_table
from app.database.database import database, metadata, engine
from app.model.params import FilterOptions, PaginationParams, SortOptions
from app.services.ingredient_service import fetch_ingredients
from app.services.recipe_service import fetch_recipes

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
async def get_recipes(
    desired_portions: Optional[float],
    sort_opts: SortOptions = Depends(),
    pagination: PaginationParams = Depends(),
    filter_opts: FilterOptions = Depends(),
):
    return await fetch_recipes(pagination, filter_opts, sort_opts, desired_portions)
    
    
@app.get("/ingredient")
async def get_ingredients(
    recipe_id: str,
    desired_portions: Optional[float]
):
    return await fetch_ingredients(recipe_id, desired_portions)