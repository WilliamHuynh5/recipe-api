import pytest
from app.model.ingredient.ingredient import Ingredient, Unit, convert


def test_convert_function():
    # mg to g
    assert convert(1000, Unit.MILLIGRAM, Unit.GRAM) == pytest.approx(1.0)
    # g to kg
    assert convert(1000, Unit.GRAM, Unit.KILOGRAM) == pytest.approx(1.0)
    # lb to oz (1 lb = 16 oz approx)
    assert convert(1, Unit.POUND, Unit.OUNCE) == pytest.approx(16.0)


def test_to_unit_method():
    ingr = Ingredient(id="ingr-1", name="Sugar", unit=Unit.GRAM, quantity=500)
    ingr.to_unit(Unit.KILOGRAM)
    assert ingr.unit == Unit.KILOGRAM
    assert ingr.name == ingr.name
    assert ingr.quantity == pytest.approx(0.5)


def test_reportion_method():
    ingr = Ingredient(id="ingr-1", name="Salt", unit=Unit.GRAM, quantity=200)
    ingr.reportion(3)
    assert ingr.quantity == 600
    assert ingr.unit == ingr.unit
    assert ingr.name == ingr.name
