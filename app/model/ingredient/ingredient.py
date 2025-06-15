from typing import Optional
from pydantic import BaseModel
from enum import Enum


# This module defines data models and unit conversion logic for recipe ingredients.
# It includes enumerations for various measurement units and types,
# designed to be highly extensible and support diverse unit categories
# such as MASS, VOLUME, and COUNT.
# The conversion logic enables transformations between compatible units.


class UnitTypes(str, Enum):
    MASS = "mass"
    VOLUME = "volume"
    COUNT = "count"


class Unit(Enum):
    def __str__(self):
        return self.value

    # Mass units (base = gram)
    MILLIGRAM = ("mg", UnitTypes.MASS, 0.001)
    GRAM = ("g", UnitTypes.MASS, 1)
    KILOGRAM = ("kg", UnitTypes.MASS, 1000)
    OUNCE = ("oz", UnitTypes.MASS, 28.3495)
    POUND = ("lb", UnitTypes.MASS, 453.592)

    # Volume units (base = milliliter)
    MILLILITER = ("ml", UnitTypes.VOLUME, 1)
    LITER = ("l", UnitTypes.VOLUME, 1000)
    FLUID_OUNCE = ("floz", UnitTypes.VOLUME, 29.5735)

    # Count units (no conversion factor)
    UNIT = ("unit", UnitTypes.COUNT, None)
    CUP = ("cup", UnitTypes.COUNT, None)
    TEASPOON = ("teaspoon", UnitTypes.COUNT, None)
    TABLESPOON = ("tablespoon", UnitTypes.COUNT, None)

    def __init__(
        self, unit_str: str, unit_type: UnitTypes, conversion_factor: Optional[float]
    ):
        self._unit_str = unit_str
        self._unit_type = unit_type
        self._conversion_factor = conversion_factor

    def __str__(self):
        return self._unit_str

    def __repr__(self):
        return f"{self._unit_str}"

    @property
    def unit_type(self) -> UnitTypes:
        return self._unit_type

    @property
    def conversion_factor(self) -> Optional[float]:
        return self._conversion_factor

    # Custom method for Pydantic to parse from string
    # Matches the string to the tuple
    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if value == member._unit_str:
                return member
        return None


def convert(quantity: float, from_unit: Unit, to_unit: Unit) -> float:
    if from_unit.unit_type != to_unit.unit_type:
        raise ValueError(
            f"Cannot convert between different unit types: {from_unit.unit_type} and {to_unit.unit_type}"
        )

    if from_unit.unit_type == UnitTypes.COUNT:
        return quantity

    base_quantity = quantity * from_unit.conversion_factor

    result = base_quantity / to_unit.conversion_factor
    return round(result, 2)


class Ingredient(BaseModel):
    id: str
    name: str
    unit: Unit
    quantity: float

    def to_unit(self, target_unit: Unit):
        if self.unit.unit_type != target_unit.unit_type:
            return

        converted_quantity = convert(self.quantity, self.unit, target_unit)
        self.unit = target_unit
        self.quantity = converted_quantity

    def reportion(self, multiplier: float):
        if multiplier <= 0:
            raise ValueError("Target portions must be greater than zero.")
        self.quantity = round(self.quantity * multiplier, 2)

    class Config:
        use_enum_values = False
        json_encoders = {Unit: lambda u: str(u)}
