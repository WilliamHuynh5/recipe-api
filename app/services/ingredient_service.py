import json
from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from app.database.database import database
from app.database.recipe_table import recipe_table
from app.model.ingredient.ingredient import Ingredient
from app.model.params import IngredientsRequest
from app.model.recipe.recipe import Recipe


from typing import List
from fastapi import HTTPException
import json
import logging


async def fetch_ingredients(req: IngredientsRequest) -> List[Ingredient]:
    if not req.recipe_id:
        raise HTTPException(status_code=400, detail="Recipe ID must be provided")

    try:
        query = select(recipe_table).where(recipe_table.c.id == req.recipe_id)
        row = await database.fetch_one(query)
    except Exception as e:
        logging.error(f"Database query failed: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    if not row:
        raise HTTPException(status_code=404, detail="Recipe not found")

    try:
        ingredients_data = json.loads(row["ingredients"])
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Corrupt ingredient data")

    try:
        recipe = Recipe(
            id=row["id"],
            name=row["name"],
            portions=row["portions"],
            ingredients=[Ingredient(**ingredient) for ingredient in ingredients_data],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to parse recipe data")

    try:
        if req.desired_portions is not None:
            recipe.reportion(req.desired_portions)
        if req.mass_unit is not None:
            recipe.reunit(req.mass_unit)
        if req.volume_unit is not None:
            recipe.reunit(req.volume_unit)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error processing recipe")

    return recipe.ingredients
