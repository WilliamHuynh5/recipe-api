import json
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import select
from app.database.database import database
from app.database.recipe_table import recipe_table
from app.model.ingredient.ingredient import Ingredient, UnitTypes
from app.model.params import IngredientsRequest
from app.model.recipe.recipe import Recipe

import logging

"""
Fetches the recipe row from the database by its ID.
"""
async def get_recipe_row_by_id(recipe_id: str) -> Optional[dict]:
    query = select(recipe_table).where(recipe_table.c.id == recipe_id)
    return await database.fetch_one(query)


"""
Retrieve and process the list of ingredients for a given recipe based on the request parameters.

This function performs the following steps:
- Validates that a recipe ID is provided.
- Queries the database to fetch the recipe row matching the given recipe ID.
- Parses the stored JSON-encoded ingredients data.
- Constructs a Recipe model including its ingredients.
- Optionally adjusts the recipe's portions if `desired_portions` is specified.
- Optionally converts ingredient units for mass and volume as specified by `mass_unit` and `volume_unit`.
- Returns the list of processed Ingredient objects.

Raises:
    HTTPException 400: If the recipe ID is missing or if invalid unit conversion is attempted.
    HTTPException 404: If no recipe is found with the given ID.
    HTTPException 500: For database errors, JSON parsing errors, or any unexpected errors during processing.

Returns:
    List[Ingredient]: A list of Ingredient models representing the processed ingredients for the recipe.
"""
async def fetch_ingredients(req: IngredientsRequest) -> List[Ingredient]:
    if not req.recipe_id:
        raise HTTPException(status_code=400, detail="Recipe ID must be provided")

    try:
        row = await get_recipe_row_by_id(req.recipe_id)
    except Exception as e:
        logging.error(f"Database query failed: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    if not row:
        raise HTTPException(status_code=404, detail="Recipe not found")

    try:
        ingredients_data = json.loads(row["ingredients"])
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse ingredient data")

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
            if req.mass_unit.unit_type != UnitTypes.MASS:
                raise ValueError(f"mass_unit must be a mass unit, got {req.mass_unit}")
            recipe.reunit(req.mass_unit)

        if req.volume_unit is not None:
            if req.volume_unit.unit_type != UnitTypes.VOLUME:
                raise ValueError(
                    f"volume_unit must be a volume unit, got {req.volume_unit}"
                )
            recipe.reunit(req.volume_unit)

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error processing recipe:, " + str(e)
        )

    return recipe.ingredients
