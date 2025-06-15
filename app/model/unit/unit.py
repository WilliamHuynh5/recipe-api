from enum import Enum


class Unit(Enum):

    def __str__(self):
        return self.code if hasattr(self, "code") else self.value

    def __repr__(self):
        return str(self)

    @classmethod
    def _missing_(cls, value: str):
        for member in cls:
            if getattr(member, "code", None) == value or member.value == value:
                return member
        return None

    def convert(self, quantity: float, to_unit: "Unit") -> float:

        if type(self) != type(to_unit):
            raise ValueError(
                f"Cannot convert between {type(self).__name__} and {type(to_unit).__name__}"
            )
        if not hasattr(self, "conversion_factor") or not hasattr(
            to_unit, "conversion_factor"
        ):
            raise ValueError("Conversion not supported for this unit type.")

        base = quantity * self.conversion_factor
        result = base / to_unit.conversion_factor
        return round(result, 2)


class MassUnit(Unit):
    """Mass units (base: gram)"""

    MILLIGRAM = ("mg", 0.001)
    GRAM = ("g", 1)
    KILOGRAM = ("kg", 1000)
    OUNCE = ("oz", 28.3495)
    POUND = ("lb", 453.592)

    def __init__(self, code: str, factor: float):
        self.code = code
        self.conversion_factor = factor


class VolumeUnit(Unit):
    """Volume units (base: milliliter)"""

    MILLILITER = ("ml", 1)
    LITER = ("l", 1000)
    FLUID_OUNCE = ("floz", 29.5735)

    def __init__(self, code: str, factor: float):
        self.code = code
        self.conversion_factor = factor


class CountUnit(Unit):
    """Countable units (not convertible)"""

    UNIT = "unit"
    CUP = "cup"
    TEASPOON = "teaspoon"
    TABLESPOON = "tablespoon"
