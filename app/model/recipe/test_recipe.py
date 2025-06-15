import pytest
from app.model.ingredient.ingredient import Ingredient, MassUnit, VolumeUnit
from app.model.recipe.recipe import Recipe


def test_reportion_method():
    # Setup quantities and portions
    flour_grams = 100
    milk_milliliters = 200
    sugar_grams = 50
    default_portions = 4
    desired_portions = 8
    multiplier = desired_portions / default_portions

    # Ingredients with different unit types: mass and volume
    ingr1 = Ingredient(
        id="ingr-1", name="Flour", unit=MassUnit.GRAM, quantity=flour_grams
    )
    ingr2 = Ingredient(
        id="ingr-2", name="Milk", unit=VolumeUnit.MILLILITER, quantity=milk_milliliters
    )
    ingr3 = Ingredient(
        id="ingr-3", name="Sugar", unit=MassUnit.GRAM, quantity=sugar_grams
    )

    recipe = Recipe(
        id="rcp-1",
        name="Cake",
        portions=default_portions,
        ingredients=[ingr1, ingr2, ingr3],
    )

    # Scale recipe portions from 4 to 8 (multiplier = 2)
    recipe.reportion(desired_portions)

    # Check updated portions and unchanged metadata
    assert recipe.portions == desired_portions
    assert recipe.id == "rcp-1"
    assert recipe.name == "Cake"

    # Check quantities scaled correctly
    assert recipe.ingredients[0].quantity == pytest.approx(flour_grams * multiplier)
    assert recipe.ingredients[1].quantity == pytest.approx(
        milk_milliliters * multiplier
    )
    assert recipe.ingredients[2].quantity == pytest.approx(sugar_grams * multiplier)

    # Check units remain unchanged
    assert recipe.ingredients[0].unit == MassUnit.GRAM
    assert recipe.ingredients[1].unit == VolumeUnit.MILLILITER
    assert recipe.ingredients[2].unit == MassUnit.GRAM


def test_reportion_invalid_portions():
    ingr = Ingredient(id="ingr-1", name="Flour", unit=MassUnit.GRAM, quantity=100)
    recipe = Recipe(id="rcp-1", name="Cake", portions=4, ingredients=[ingr])

    # Target portions <= 0 should raise ValueError
    with pytest.raises(ValueError):
        recipe.reportion(0)
    with pytest.raises(ValueError):
        recipe.reportion(-2)
