import pytest
from unittest.mock import patch, AsyncMock
from fastapi import HTTPException
from app.model.ingredient.ingredient import Unit
from app.model.params import IngredientsRequest
from app.services.ingredient_service import fetch_ingredients

@pytest.mark.asyncio
@patch("app.services.ingredient_service.database.fetch_one", new_callable=AsyncMock)
async def test_fetch_ingredients_returns_ingredients(mock_fetch_one):
    mock_fetch_one.return_value = {
        "id": "r1",
        "name": "Test Recipe",
        "portions": 4,
        "ingredients": '[{"name":"Sugar","quantity":100,"unit":"g"}]'
    }

    req = IngredientsRequest(recipe_id="r1")
    ingredients = await fetch_ingredients(req)

    mock_fetch_one.assert_awaited_once()

    assert len(ingredients) == 1
    assert ingredients[0].name == "Sugar"
    assert ingredients[0].quantity == 100
    assert ingredients[0].unit == Unit.GRAM
    
    
@pytest.mark.asyncio
@patch("app.services.ingredient_service.database.fetch_one", new_callable=AsyncMock)
async def test_fetch_ingredients_returns_ingredients_double_portions(mock_fetch_one):
    mock_fetch_one.return_value = {
        "id": "r1",
        "name": "Test Recipe",
        "portions": 4,
        "ingredients": '[{"name":"Sugar","quantity":100,"unit":"g"}]'
    }

    req = IngredientsRequest(recipe_id="r1", desired_portions=8)
    ingredients = await fetch_ingredients(req)

    mock_fetch_one.assert_awaited_once()

    assert len(ingredients) == 1
    assert ingredients[0].name == "Sugar"
    # Double the normal 100 grams
    assert ingredients[0].quantity == 200 
    assert ingredients[0].unit == Unit.GRAM
    
    
@pytest.mark.asyncio
@patch("app.services.ingredient_service.database.fetch_one", new_callable=AsyncMock)
async def test_fetch_ingredients_returns_ingredients_kg_preferred(mock_fetch_one):
    mock_fetch_one.return_value = {
        "id": "r1",
        "name": "Test Recipe",
        "portions": 4,
        "ingredients": '[{"name":"Sugar","quantity":100,"unit":"g"}]'
    }

    req = IngredientsRequest(recipe_id="r1", mass_unit='kg')
    ingredients = await fetch_ingredients(req)

    mock_fetch_one.assert_awaited_once()

    assert len(ingredients) == 1
    assert ingredients[0].name == "Sugar"
    assert ingredients[0].quantity == 0.1
    assert ingredients[0].unit == Unit.KILOGRAM
    
@pytest.mark.asyncio
@patch("app.services.ingredient_service.database.fetch_one", new_callable=AsyncMock)
async def test_fetch_ingredients_returns_ingredients_oz_preferred(mock_fetch_one):
    mock_fetch_one.return_value = {
        "id": "r1",
        "name": "Test Recipe",
        "portions": 4,
        "ingredients": '[{"name":"Lemon Juice","quantity":100,"unit":"ml"}]'
    }

    req = IngredientsRequest(recipe_id="r1", volume_unit='floz')
    ingredients = await fetch_ingredients(req)

    mock_fetch_one.assert_awaited_once()

    assert len(ingredients) == 1
    assert ingredients[0].name == "Lemon Juice"
    assert ingredients[0].quantity == 3.38
    assert ingredients[0].unit == Unit.FLUID_OUNCE
    
@pytest.mark.asyncio
@patch("app.services.ingredient_service.database.fetch_one", new_callable=AsyncMock)
async def test_fetch_ingredients_returns_ingredients_kg_oz_preferred(mock_fetch_one):
    mock_fetch_one.return_value = {
        "id": "r1",
        "name": "Test Recipe",
        "portions": 4,
        "ingredients": '[{"name":"Lemon Juice","quantity":100,"unit":"ml"}, {"name":"Sugar","quantity":100,"unit":"g"}]'
    }

    req = IngredientsRequest(recipe_id="r1", mass_unit="kg", volume_unit='floz')
    ingredients = await fetch_ingredients(req)

    mock_fetch_one.assert_awaited_once()

    assert len(ingredients) == 2
    assert ingredients[0].name == "Lemon Juice"
    assert ingredients[0].quantity == 3.38
    assert ingredients[0].unit == Unit.FLUID_OUNCE

    assert ingredients[1].name == "Sugar"
    assert ingredients[1].quantity == 0.1
    assert ingredients[1].unit == Unit.KILOGRAM
    
@pytest.mark.asyncio
@patch("app.services.ingredient_service.database.fetch_one", new_callable=AsyncMock)
async def test_fetch_ingredients_returns_ingredients_countable_unaffected(mock_fetch_one):
    mock_fetch_one.return_value = {
        "id": "r1",
        "name": "Test Recipe",
        "portions": 4,
        "ingredients": '[{"name":"Lemon Juice","quantity":1,"unit":"cup"}]'
    }

    req = IngredientsRequest(recipe_id="r1", volume_unit='floz')
    ingredients = await fetch_ingredients(req)

    mock_fetch_one.assert_awaited_once()

    assert len(ingredients) == 1
    assert ingredients[0].name == "Lemon Juice"
    assert ingredients[0].quantity == 1
    assert ingredients[0].unit == Unit.CUP


@pytest.mark.asyncio
@patch("app.services.ingredient_service.database.fetch_one", new_callable=AsyncMock)
async def test_fetch_ingredients_recipe_not_exist(mock_fetch_one):
    
    mock_fetch_one.return_value = None

    req = IngredientsRequest(recipe_id="Doesn't Exist")

    with pytest.raises(HTTPException) as exc:
        await fetch_ingredients(req)
    assert exc.value.status_code == 404
    assert exc.value.detail == "Recipe not found"
    
    
@pytest.mark.asyncio
@patch("app.services.ingredient_service.database.fetch_one", new_callable=AsyncMock)
async def test_fetch_ingredients_recipe_corrupt_ingredients_data(mock_fetch_one):
    
    mock_fetch_one.return_value = {
        "id": "r1",
        "name": "Test Recipe",
        "portions": 4,
        "ingredients": '["""""{"name":"Sugar","quantity":100,"unit":"g"}"""""]'
    }

    req = IngredientsRequest(recipe_id="r1")

    with pytest.raises(HTTPException) as exc:
        await fetch_ingredients(req)
    assert exc.value.status_code == 500
    assert exc.value.detail == "Failed to parse ingredient data"


@pytest.mark.asyncio
@patch("app.services.ingredient_service.database.fetch_one", new_callable=AsyncMock)
async def test_fetch_ingredients_recipe_corrupt_recipe_data(mock_fetch_one):
    
    # Missing the name and portions field
    mock_fetch_one.return_value = {
        "id": "r1",
        "ingredients": '[{"name":"Sugar","quantity":100,"unit":"g"}]'
    }

    req = IngredientsRequest(recipe_id="r1")

    with pytest.raises(HTTPException) as exc:
        await fetch_ingredients(req)
    assert exc.value.status_code == 500
    assert exc.value.detail == "Failed to parse recipe data"
    
    
@pytest.mark.asyncio
@patch("app.services.ingredient_service.database.fetch_one", new_callable=AsyncMock)
async def test_fetch_ingredients_recipe_invalid_mass_unit(mock_fetch_one):
    
    mock_fetch_one.return_value = {
        "id": "r1",
        "name": "Test Recipe",
        "portions": 4,
        "ingredients": '[{"name":"Sugar","quantity":100,"unit":"g"}]'
    }
    
    # Passing milliliters as mass_unit
    req = IngredientsRequest(recipe_id="r1", mass_unit="ml")

    with pytest.raises(HTTPException) as exc:
        await fetch_ingredients(req)
    assert exc.value.status_code == 400
    assert exc.value.detail == "mass_unit must be a mass unit, got ml"
    
    
@pytest.mark.asyncio
@patch("app.services.ingredient_service.database.fetch_one", new_callable=AsyncMock)
async def test_fetch_ingredients_recipe_invalid_volume_unit(mock_fetch_one):
    
    mock_fetch_one.return_value = {
        "id": "r1",
        "name": "Test Recipe",
        "portions": 4,
        "ingredients": '[{"name":"Sugar","quantity":100,"unit":"g"}]'
    }
    
    # Passing kg as volume_unit
    req = IngredientsRequest(recipe_id="r1", volume_unit="kg")

    with pytest.raises(HTTPException) as exc:
        await fetch_ingredients(req)
    assert exc.value.status_code == 400
    assert exc.value.detail == "volume_unit must be a volume unit, got kg"