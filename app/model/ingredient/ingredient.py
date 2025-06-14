from pydantic import BaseModel
from enum import Enum


class Unit(Enum):
    MILLIGRAM = "mg"
    GRAM = "g"
    KILOGRAM = "kg"
    OUNCE = "oz"
    POUND = "lb"


CONVERSION_TO_GRAMS = {
    Unit.MILLIGRAM: 0.001,
    Unit.GRAM: 1,
    Unit.KILOGRAM: 1000,
    Unit.OUNCE: 28.3495,
    Unit.POUND: 453.592,
}


def convert(quantity: float, from_unit: Unit, to_unit: Unit) -> float:
    in_grams = quantity * CONVERSION_TO_GRAMS[from_unit]
    return in_grams / CONVERSION_TO_GRAMS[to_unit]


class Ingredient(BaseModel):
    id: str;
    name: str
    unit: Unit
    quantity: float

    def to_unit(self, target_unit: Unit) -> "Ingredient":
        converted_quantity = convert(self.quantity, self.unit, target_unit)
        return Ingredient(id=self.id, name=self.name, unit=target_unit, quantity=converted_quantity)

    def reportion(self, multiplier: float) -> "Ingredient":
        return Ingredient(
            id=self.id, name=self.name, unit=self.unit, quantity=self.quantity * multiplier
        )
