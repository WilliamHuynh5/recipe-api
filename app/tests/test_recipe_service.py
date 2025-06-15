import pytest
from unittest.mock import patch, AsyncMock
from fastapi import HTTPException
from app.model.ingredient.ingredient import Unit
from app.model.params import PaginationParams, FilterOptions, SortOptions, SortOrder, RecipesRequest
from app.services.recipe_service import fetch_recipes

@pytest.mark.asyncio
@patch("app.services.recipe_service.database.fetch_all", new_callable=AsyncMock)
async def test_fetch_recipes_returns_recipes(mock_fetch_all):
    
    mock_fetch_all.return_value = [
        {
            "id": "r1",
            "name": "Test Recipe",
            "portions": 4,
            "ingredients": '[{"name": "Sugar", "quantity": 100, "unit": "g"}]'
        }
    ]

    pagination = PaginationParams(page=1, size=5)
    filter_opts = FilterOptions(queryString=None)
    sort_opts = SortOptions(field="portions", order=SortOrder.ASC)
    req = RecipesRequest()

    response = await fetch_recipes(pagination, filter_opts, sort_opts, req)

    mock_fetch_all.assert_awaited_once()

    assert response.page == 1
    assert response.size == 5
    assert len(response.items) == 1

    recipe = response.items[0]
    assert recipe.id == "r1"
    assert recipe.name == "Test Recipe"
    assert recipe.portions == 4
    assert len(recipe.ingredients) == 1
    
    ingredient = recipe.ingredients[0]
    assert ingredient.name == "Sugar"
    assert ingredient.quantity == 100
    assert ingredient.unit == Unit.GRAM

@pytest.mark.asyncio
@patch("app.services.recipe_service.database.fetch_all", new_callable=AsyncMock)
async def test_fetch_recipes_with_double_portion_and_mass_unit_conversion(mock_fetch_all):
    mock_fetch_all.return_value = [
        {
            "id": "r1",
            "name": "Test Recipe",
            "portions": 4,
            "ingredients": '[{"name": "Sugar", "quantity": 100, "unit": "g"}]'
        }
    ]

    pagination = PaginationParams()
    filter_opts = None
    sort_opts = None
    # Double the portions of the recipe
    # Also preferred mass unit in Kilograms
    req = RecipesRequest(desired_portions=8, mass_unit=Unit.KILOGRAM)

    response = await fetch_recipes(pagination, filter_opts, sort_opts, req)

    mock_fetch_all.assert_awaited_once()

    recipe = response.items[0]
    assert recipe.portions == 8
    
    ingredient = recipe.ingredients[0]
    assert ingredient.name == "Sugar"
    assert ingredient.quantity == 0.2
    assert ingredient.unit == Unit.KILOGRAM
    
@pytest.mark.asyncio
@patch("app.services.recipe_service.database.fetch_all", new_callable=AsyncMock)
async def test_fetch_recipes_with_double_portion_and_volume_unit_conversion(mock_fetch_all):
    mock_fetch_all.return_value = [
        {
            "id": "r1",
            "name": "Test Recipe",
            "portions": 4,
            "ingredients": '[{"name": "Sugar", "quantity": 100, "unit": "ml"}]'
        }
    ]

    pagination = PaginationParams()
    filter_opts = None
    sort_opts = None
    # Double the portions of the recipe
    # Also preferred mass unit in Kilograms
    req = RecipesRequest(desired_portions=8, volume_unit=Unit.LITER)

    response = await fetch_recipes(pagination, filter_opts, sort_opts, req)

    mock_fetch_all.assert_awaited_once()

    recipe = response.items[0]
    assert recipe.portions == 8
    
    ingredient = recipe.ingredients[0]
    assert ingredient.name == "Sugar"
    assert ingredient.quantity == 0.2
    assert ingredient.unit == Unit.LITER

@pytest.mark.asyncio
@patch("app.services.recipe_service.database.fetch_all", new_callable=AsyncMock)
async def test_fetch_recipes_invalid_mass_unit(mock_fetch_all):
    mock_fetch_all.return_value = [
        {
            "id": "r1",
            "name": "Test Recipe",
            "portions": 4,
            "ingredients": '[{"name": "Sugar", "quantity": 100, "unit": "g"}]'
        }
    ]

    pagination = PaginationParams()
    filter_opts = None
    sort_opts = None
    
     # invalid mass unit
    req = RecipesRequest(mass_unit=Unit.MILLILITER) 

    with pytest.raises(HTTPException) as exc:
        await fetch_recipes(pagination, filter_opts, sort_opts, req)
    assert exc.value.status_code == 400
    assert "mass_unit must be a mass unit" in exc.value.detail
