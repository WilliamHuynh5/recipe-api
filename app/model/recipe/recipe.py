from typing import List
from pydantic import BaseModel
from app.model.ingredient.ingredient import Ingredient, Unit


class Recipe(BaseModel):
    id: str
    name: str
    portions: float
    ingredients: List[Ingredient]

    def reunit(self, target_unit: Unit):
        for ingredient in self.ingredients:
            ingredient.to_unit(target_unit)

    def reportion(self, target_portions: float):
        if target_portions <= 0:
            raise ValueError("Target portions must be greater than zero.")

        multiplier = target_portions / self.portions
        for ingredient in self.ingredients:
            ingredient.reportion(multiplier)

        self.portions = target_portions
