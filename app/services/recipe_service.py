import json
from typing import Optional
from sqlalchemy import select, desc, asc, func
from app.database.database import database
from app.database.recipe_table import recipe_table
from app.model.ingredient.ingredient import Ingredient
from app.model.params import (
    FilterOptions,
    PaginationParams,
    RecipesRequest,
    SortOptions,
    SortOrder,
)
from app.model.recipe.recipe import Recipe
from app.utils.pagination import PaginatedResponse


async def fetch_recipes(
    pagination: PaginationParams = PaginationParams(),
    filter_opts: Optional[FilterOptions] = None,
    sort_opts: Optional[SortOptions] = None,
    req: Optional[RecipesRequest] = None,
) -> PaginatedResponse[Recipe]:
    query = select(recipe_table)

    # Filtering
    if filter_opts and filter_opts.queryString:
        query = query.where(recipe_table.c.name.ilike(f"%{filter_opts.queryString}%"))

    # Sorting
    if sort_opts:
        allowed_fields = {"portions"}
        if sort_opts.field in allowed_fields:
            sort_column = getattr(recipe_table.c, sort_opts.field)
            order_method = desc if sort_opts.order == SortOrder.DESC else asc
            query = query.order_by(order_method(sort_column))

    count_query = select(func.count()).select_from(recipe_table)
    if filter_opts and filter_opts.queryString:
        count_query = count_query.where(
            recipe_table.c.name.ilike(f"%{filter_opts.queryString}%")
        )

    # Pagination
    query = query.offset(pagination.offset).limit(pagination.size)

    rows = await database.fetch_all(query)

    recipes = []
    for row in rows:
        recipe = Recipe(
            id=row["id"],
            name=row["name"],
            portions=row["portions"],
            ingredients=[
                Ingredient(**ingredient)
                for ingredient in json.loads(row["ingredients"])
            ],
        )
        if req.desired_portions is not None:
            recipe.reportion(req.desired_portions)
        if req.desired_unit is not None:
            recipe.reunit(req.desired_unit)
        recipes.append(recipe)

    return recipes
