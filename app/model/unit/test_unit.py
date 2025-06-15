import pytest
from app.model.ingredient.ingredient import MassUnit, VolumeUnit, CountUnit


def test_unit_str_and_repr() -> None:
    assert str(MassUnit.GRAM) == "g"
    assert repr(MassUnit.GRAM) == "g"
    assert str(VolumeUnit.LITER) == "l"
    assert str(CountUnit.CUP) == "cup"
    assert repr(CountUnit.UNIT) == "unit"


def test_massunit_conversion() -> None:
    assert MassUnit.MILLIGRAM.convert(1000, MassUnit.GRAM) == pytest.approx(1.0)
    assert MassUnit.GRAM.convert(5000, MassUnit.KILOGRAM) == pytest.approx(5.0)
    assert MassUnit.POUND.convert(1, MassUnit.OUNCE) == pytest.approx(16.0)


def test_volumeunit_conversion() -> None:
    assert VolumeUnit.LITER.convert(1, VolumeUnit.MILLILITER) == pytest.approx(1000.0)
    assert VolumeUnit.FLUID_OUNCE.convert(2, VolumeUnit.MILLILITER) == pytest.approx(
        59.15, rel=1e-2
    )


def test_zero_quantity_conversion() -> None:
    assert MassUnit.GRAM.convert(0, MassUnit.KILOGRAM) == 0
    assert VolumeUnit.LITER.convert(0, VolumeUnit.MILLILITER) == 0


def test_countunit_identity() -> None:
    assert CountUnit.UNIT == CountUnit.UNIT
    assert str(CountUnit.TEASPOON) == "teaspoon"


def test_countunit_conversion_unsupported() -> None:
    with pytest.raises(
        ValueError, match="Conversion not supported for this unit type."
    ):
        CountUnit.CUP.convert(1, CountUnit.TABLESPOON)


def test_cross_type_conversion_error() -> None:
    with pytest.raises(
        ValueError, match="Cannot convert between MassUnit and VolumeUnit"
    ):
        MassUnit.GRAM.convert(100, VolumeUnit.LITER)

    with pytest.raises(
        ValueError, match="Cannot convert between CountUnit and MassUnit"
    ):
        CountUnit.UNIT.convert(1, MassUnit.GRAM)


def test_unit_missing_method() -> None:
    assert MassUnit._missing_("g") == MassUnit.GRAM
    assert VolumeUnit._missing_("ml") == VolumeUnit.MILLILITER
    assert CountUnit._missing_("cup") == CountUnit.CUP
    assert CountUnit._missing_("nonexistent") is None
