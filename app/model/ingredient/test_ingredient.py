import pytest
from app.model.ingredient.ingredient import Ingredient, Unit, convert
from app.model.ingredient.ingredient import UnitTypes  # if needed


def test_convert_function_basic() -> None:
    # Basic valid conversions
    assert convert(1000, Unit.MILLIGRAM, Unit.GRAM) == pytest.approx(1.0)
    assert convert(1000, Unit.GRAM, Unit.KILOGRAM) == pytest.approx(1.0)
    assert convert(1, Unit.POUND, Unit.OUNCE) == pytest.approx(16.0)


def test_convert_function_count_units() -> None:
    # COUNT units convert to same quantity (no conversion)
    assert convert(5, Unit.UNIT, Unit.UNIT) == 5
    assert convert(10, Unit.CUP, Unit.CUP) == 10
    assert (
        convert(3, Unit.TABLESPOON, Unit.TEASPOON) == 3
    )  # Different count units, should behave same


def test_convert_function_type_mismatch() -> None:
    # Converting between different unit types should raise ValueError
    with pytest.raises(ValueError):
        convert(1, Unit.GRAM, Unit.MILLILITER)
    with pytest.raises(ValueError):
        convert(1, Unit.UNIT, Unit.GRAM)
    with pytest.raises(ValueError):
        convert(1, Unit.CUP, Unit.GRAM)


def test_convert_function_zero_quantity() -> None:
    # Zero quantity should convert to zero regardless of units
    assert convert(0, Unit.GRAM, Unit.KILOGRAM) == 0
    assert convert(0, Unit.UNIT, Unit.CUP) == 0


def test_ingredient_to_unit_valid_conversion() -> None:
    ingredient = Ingredient(name="Sugar", unit=Unit.GRAM, quantity=500.0)
    ingredient.to_unit(Unit.KILOGRAM)
    assert ingredient.unit == Unit.KILOGRAM
    assert ingredient.quantity == pytest.approx(0.5)


def test_ingredient_to_unit_invalid_conversion() -> None:
    ingredient = Ingredient(name="Water", unit=Unit.MILLILITER, quantity=1000.0)
    # Should not convert because unit types differ (MILLILITER is VOLUME, GRAM is MASS)
    ingredient.to_unit(Unit.GRAM)
    # Values unchanged
    assert ingredient.unit == Unit.MILLILITER
    assert ingredient.quantity == pytest.approx(1000.0)


def test_ingredient_reportion() -> None:
    ingredient = Ingredient(name="Salt", unit=Unit.GRAM, quantity=200.0)
    ingredient.reportion(3.0)
    assert ingredient.quantity == pytest.approx(600.0)


def test_ingredient_reportion_zero_multiplier() -> None:
    ingredient = Ingredient(name="Pepper", unit=Unit.GRAM, quantity=50.0)
    with pytest.raises(ValueError, match="Target portions must be greater than zero."):
        ingredient.reportion(0)


def test_ingredient_reportion_negative_multiplier() -> None:
    ingredient = Ingredient(name="Chili", unit=Unit.GRAM, quantity=10.0)
    with pytest.raises(ValueError, match="Target portions must be greater than zero."):
        ingredient.reportion(-2)


def test_unit_missing_method() -> None:
    # Test that _missing_ allows parsing from string to Unit enum
    assert Unit._missing_("g") == Unit.GRAM
    assert Unit._missing_("cup") == Unit.CUP
    # Invalid string returns None
    assert Unit._missing_("unknown") is None


def test_unit_str_and_repr() -> None:
    # Test string and repr methods return the string representation of unit
    assert str(Unit.KILOGRAM) == "kg"
    assert repr(Unit.KILOGRAM) == "kg"
