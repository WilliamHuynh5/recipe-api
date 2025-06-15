from typing import Optional
from pydantic import BaseModel
from enum import Enum

"""
This module defines data models and unit conversion logic for recipe ingredients.
It includes enumerations for various measurement units and types,
designed to be highly extensible and support diverse unit categories
such as MASS, VOLUME, and COUNT.
The conversion logic enables transformations between compatible units.
"""


"""
Enum of unit categories used to classify measurement units.

This enum helps determine compatibility for unit conversions.
Currently, it defines three types:

- MASS: Units measuring weight/mass (e.g., grams, pounds).
- VOLUME: Units measuring volume (e.g., milliliters).
- COUNT: Countable units without conversion factors (e.g., units, teaspoons).

Units of different types are not convertible to each other.
"""
class UnitTypes(str, Enum):
    MASS = "mass"
    VOLUME = "volume"
    COUNT = "count"

"""
Enum representing measurement units used for ingredients.

Each unit is represented as a tuple containing:
- A unique unit code (string),
- The unit type (UnitTypes enum) indicating the category (mass, volume, count),
- A conversion factor to the base unit in grams (mass) or milliliters (volume),
  or None if no conversion is applicable (e.g., count units).

This enum supports:
- String representation matching the unique unit code,
- Properties for accessing the unit type and conversion factor,
- A custom Pydantic-compatible `_missing_` method to parse unit strings back to enum members.
"""
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
    # Matches the string to the tuple. i.e we can use the unique unit code
    # to match to the tuple.
    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if value == member._unit_str:
                return member
        return None


"""
Convert a quantity from one unit to another, ensuring unit types match.

Parameters:
    quantity (float): The numeric amount to convert.
    from_unit (Unit): The unit of the original quantity.
    to_unit (Unit): The unit to convert the quantity into.

Returns:
    float: The converted quantity, rounded to 2 decimal places.

Raises:
    ValueError: If `from_unit` and `to_unit` are of different unit types,
                meaning conversion between them is not valid.

Notes:
    - If the unit type is COUNT (e.g., discrete items), the quantity is returned unchanged.
    - Conversion is done via a base unit using `conversion_factor` attributes on units.
"""
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


"""
Represents an ingredient with a specific quantity and measurement unit.

Attributes:
    id (str): Unique identifier for the ingredient.
    name (str): The name of the ingredient (e.g., "sugar", "flour").
    unit (Unit): The unit of measurement for the quantity.
    quantity (float): The amount of the ingredient in the specified unit.

Methods:
    to_unit(target_unit: Unit):
        Converts the ingredient's quantity to a different unit if compatible.
        If the target unit's type differs, no conversion is performed.

    reportion(multiplier: float):
        Scales the ingredient quantity by a multiplier.
        Raises ValueError if the multiplier is zero or negative.

Config:
    use_enum_values (bool): When serialising, enums are not replaced by their values.
    json_encoders (dict): Custom JSON encoder for Unit to serialize it as string.
"""
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
