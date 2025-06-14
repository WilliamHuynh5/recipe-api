import json
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import select
from app.database.database import database 
from app.database.recipe_table import recipe_table
from app.model.ingredient.ingredient import Ingredient
from app.model.recipe.recipe import Recipe


async def fetch_ingredients(recipe_id: str, desired_portions: Optional[float] = None) -> List[Ingredient]:
    query = select(recipe_table).where(recipe_table.c.id == recipe_id)
    row = await database.fetch_one(query)

    if not row:
        raise HTTPException(status_code=404, detail="Recipe not found")

    recipe = Recipe(
        id=row["id"],
        name=row["name"],
        portions=row["portions"],
        ingredients=[Ingredient(**ingredient) for ingredient in json.loads(row["ingredients"])]
    )
    if desired_portions != None:
        recipe.reportion(desired_portions);
    
    return recipe.ingredients

