import json
from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from app.database.database import database
from app.database.recipe_table import recipe_table
from app.model.ingredient.ingredient import Ingredient
from app.model.params import IngredientsRequest
from app.model.recipe.recipe import Recipe


async def fetch_ingredients(req: IngredientsRequest) -> List[Ingredient]:

    query = select(recipe_table).where(recipe_table.c.id == req.recipe_id)
    row = await database.fetch_one(query)

    if not row:
        raise HTTPException(status_code=404, detail="Recipe not found")

    recipe = Recipe(
        id=row["id"],
        name=row["name"],
        portions=row["portions"],
        ingredients=[
            Ingredient(**ingredient) for ingredient in json.loads(row["ingredients"])
        ],
    )
    if req.desired_portions != None:
        recipe.reportion(req.desired_portions)
    if req.desired_unit != None:
        recipe.reunit(req.desired_unit)

    return recipe.ingredients
