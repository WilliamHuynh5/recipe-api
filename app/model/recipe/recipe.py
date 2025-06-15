from typing import List
from pydantic import BaseModel
from app.model.ingredient.ingredient import Ingredient, Unit


class Recipe(BaseModel):
    id: str
    name: str
    portions: float
    ingredients: List[Ingredient]

    def reunit(self, target_unit: Unit):
        if not isinstance(target_unit, Unit):
            raise ValueError(
                f"Invalid target_unit: expected Unit enum, got {type(target_unit)}"
            )

        for ingredient in self.ingredients:
            ingredient.to_unit(target_unit)

    def reportion(self, target_portions: float):
        if target_portions <= 0:
            raise ValueError("Target portions must be greater than zero.")

        multiplier = target_portions / self.portions
        for ingredient in self.ingredients:
            ingredient.reportion(multiplier)

        self.portions = target_portions
