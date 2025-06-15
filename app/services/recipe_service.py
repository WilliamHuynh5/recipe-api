import json
from typing import Optional
from fastapi import HTTPException
from sqlalchemy import Select, select, desc, asc, func
from app.database.database import database
from app.database.recipe_table import recipe_table
from app.model.ingredient.ingredient import Ingredient, UnitTypes
from app.model.params import (
    FilterOptions,
    PaginationParams,
    RecipesRequest,
    SortOptions,
    SortOrder,
)
from app.model.recipe.recipe import Recipe
from app.utils.pagination import PaginatedResponse
"""
Fetches the recipes from the database. Has filtering, sorting and pagination.
"""
async def get_recipes(
    pagination: PaginationParams,
    filter_opts: Optional[FilterOptions] = None,
    sort_opts: Optional[SortOptions] = None,
) -> Select:
    query = select(recipe_table)

    # Handle filtering
    if filter_opts and filter_opts.queryString:
        query = query.where(recipe_table.c.name.ilike(f"%{filter_opts.queryString}%"))

    # Handle sorting
    if sort_opts:
        allowed_fields = {"portions"}
        if sort_opts.field in allowed_fields:
            sort_column = getattr(recipe_table.c, sort_opts.field)
            order_method = desc if sort_opts.order == SortOrder.DESC else asc
            query = query.order_by(order_method(sort_column))

    # Apply pagination
    query = query.offset(pagination.offset).limit(pagination.size)
    return await database.fetch_all(query)


"""
Fetch a paginated list of recipes from the database with optional filtering, sorting, and portion/unit adjustments.

This function:
- Applies an optional filter on recipe names using a case-insensitive search query.
- Applies optional sorting on allowed fields (currently only 'portions').
- Applies pagination to limit the number of results returned.
- Parses each recipe's ingredient JSON data into Ingredient objects.
- Optionally adjusts each recipe's ingredient quantities for desired portions and unit conversions.
- Returns a paginated response containing the processed recipes.

Args:
    pagination (PaginationParams, optional): Pagination parameters (page number and page size). Defaults to first page with size 5.
    filter_opts (Optional[FilterOptions], optional): Filter options including query string for searching recipe names.
    sort_opts (Optional[SortOptions], optional): Sorting options specifying field and order (ascending/descending).
    req (Optional[RecipesRequest], optional): Optional recipe-related parameters for desired portions and unit conversions.

Raises:
    HTTPException 400: If invalid unit conversions or portion adjustments are requested.
    HTTPException 500: For unexpected errors during recipe processing.

Returns:
    PaginatedResponse[Recipe]: A paginated list of Recipe models matching the query with applied adjustments.
"""


async def fetch_recipes(
    pagination: PaginationParams = PaginationParams(),
    filter_opts: Optional[FilterOptions] = None,
    sort_opts: Optional[SortOptions] = None,
    req: Optional[RecipesRequest] = None,
) -> PaginatedResponse[Recipe]:

    
    try:
        rows = await get_recipes(pagination, filter_opts, sort_opts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

    recipes = []
    for row in rows:
        try:
            recipe = Recipe(
                id=row["id"],
                name=row["name"],
                portions=row["portions"],
                ingredients=[
                    Ingredient(**ingredient)
                    for ingredient in json.loads(row["ingredients"])
                ],
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to parse recipe data")
            
        try:
            if req and req.desired_portions is not None:
                recipe.reportion(req.desired_portions)
            if req and req.mass_unit is not None:
                if req.mass_unit.unit_type != UnitTypes.MASS:
                    raise ValueError(f"mass_unit must be a mass unit, got {req.mass_unit}")
                recipe.reunit(req.mass_unit)

            if req and req.volume_unit is not None:
                if req.volume_unit.unit_type != UnitTypes.VOLUME:
                    raise ValueError(
                        f"volume_unit must be a volume unit, got {req.volume_unit}"
                    )
                recipe.reunit(req.volume_unit)
            recipes.append(recipe)
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))
        except Exception:
            raise HTTPException(status_code=500, detail="Error processing recipe")

    return PaginatedResponse[Recipe](
        page=pagination.page,
        size=pagination.size,
        items=recipes,
    )