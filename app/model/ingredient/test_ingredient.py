import pytest
from app.model.ingredient.ingredient import (
    Ingredient,
    MassUnit,
    VolumeUnit,
    CountUnit,
)


def test_massunit_conversion() -> None:
    assert MassUnit.MILLIGRAM.convert(1000, MassUnit.GRAM) == pytest.approx(1.0)
    assert MassUnit.GRAM.convert(1000, MassUnit.KILOGRAM) == pytest.approx(1.0)
    assert MassUnit.POUND.convert(1, MassUnit.OUNCE) == pytest.approx(16.0)


def test_volumeunit_conversion() -> None:
    assert VolumeUnit.LITER.convert(1, VolumeUnit.MILLILITER) == pytest.approx(1000.0)
    assert VolumeUnit.FLUID_OUNCE.convert(2, VolumeUnit.MILLILITER) == pytest.approx(
        59.15
    )


def test_countunit_no_conversion() -> None:
    assert CountUnit.UNIT == CountUnit.UNIT
    assert str(CountUnit.CUP) == "cup"


def test_zero_quantity_conversion() -> None:
    assert MassUnit.GRAM.convert(0, MassUnit.KILOGRAM) == 0
    assert VolumeUnit.LITER.convert(0, VolumeUnit.MILLILITER) == 0


def test_ingredient_to_unit_success() -> None:
    ingredient = Ingredient(name="Flour", unit=MassUnit.GRAM, quantity=500)
    ingredient.to_unit(MassUnit.KILOGRAM)
    assert ingredient.unit == MassUnit.KILOGRAM
    assert ingredient.quantity == pytest.approx(0.5)


def test_ingredient_reportion() -> None:
    ingredient = Ingredient(name="Butter", unit=MassUnit.GRAM, quantity=200)
    ingredient.reportion(2.5)
    assert ingredient.quantity == pytest.approx(500.0)


def test_ingredient_reportion_invalid_multiplier() -> None:
    ingredient = Ingredient(name="Salt", unit=MassUnit.GRAM, quantity=100)
    with pytest.raises(ValueError):
        ingredient.reportion(0)
    with pytest.raises(ValueError):
        ingredient.reportion(-1)


def test_unit_str_repr_and_missing() -> None:
    # Confirm string and repr return correct values
    assert str(MassUnit.GRAM) == "g"
    assert repr(MassUnit.GRAM) == "g"
    assert str(VolumeUnit.LITER) == "l"
    assert str(CountUnit.TEASPOON) == "teaspoon"

    # _missing_ method
    assert MassUnit._missing_("g") == MassUnit.GRAM
    assert VolumeUnit._missing_("ml") == VolumeUnit.MILLILITER
    assert CountUnit._missing_("cup") == CountUnit.CUP
    assert CountUnit._missing_("unknown one") is None
