from typing import Union
from pydantic import BaseModel
from app.model.unit.unit import CountUnit, MassUnit, Unit, VolumeUnit


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
    name: str
    unit: Union[MassUnit, VolumeUnit, CountUnit]
    quantity: float

    def to_unit(self, target_unit: Unit):
        if not hasattr(self.unit, "convert"):
            raise ValueError("This unit type does not support conversion.")

        if type(self.unit) == type(target_unit):
            self.quantity = self.unit.convert(self.quantity, target_unit)
            self.unit = target_unit

    def reportion(self, multiplier: float):
        if multiplier <= 0:
            raise ValueError("Target portions must be greater than zero.")
        self.quantity = round(self.quantity * multiplier, 2)

    class Config:
        use_enum_values = False
        json_encoders = {
            MassUnit: lambda u: str(u),
            VolumeUnit: lambda u: str(u),
            CountUnit: lambda u: str(u),
        }
