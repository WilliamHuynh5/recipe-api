import pytest
from app.model.ingredient.ingredient import Ingredient, Unit
from app.model.recipe.recipe import Recipe


def test_reportion_method():
    flour_grams = 100
    sugar_grams = 50
    defaultPortions = 4
    desiredPortions = 8
    multiplier = desiredPortions / defaultPortions

    ingr1 = Ingredient(name="Flour", unit=Unit.GRAM, quantity=flour_grams)
    ingr2 = Ingredient(name="Sugar", unit=Unit.GRAM, quantity=sugar_grams)
    recipe = Recipe(
        id=1, name="Cake", portions=defaultPortions, quantity=[ingr1, ingr2]
    )

    # Scale from 4 portions to 8 portions (multiplier = 8 / 2 = 2)
    scaled = recipe.reportion(desiredPortions)
    assert scaled.portions == desiredPortions
    assert scaled.id == recipe.id
    assert scaled.name == recipe.name

    # Each ingredient quantity should be "multiplied" correctly
    assert scaled.quantity[0].quantity == pytest.approx(flour_grams * multiplier)
    assert scaled.quantity[1].quantity == pytest.approx(sugar_grams * multiplier)
    assert scaled.quantity[0].unit == ingr1.unit
    assert scaled.quantity[1].unit == ingr2.unit


def test_reportion_invalid_portions():
    ingr = Ingredient(name="Flour", unit=Unit.GRAM, quantity=100)
    recipe = Recipe(id=1, name="Cake", portions=4, quantity=[ingr])

    # Target portions <= 0 should raise ValueError
    with pytest.raises(ValueError):
        recipe.reportion(0)
    with pytest.raises(ValueError):
        recipe.reportion(-2)
