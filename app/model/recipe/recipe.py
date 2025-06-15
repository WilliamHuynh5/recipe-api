from typing import List
from pydantic import BaseModel
from app.model.ingredient.ingredient import Ingredient, Unit


"""
Represents a cooking recipe, including its ingredients and portion size.

Attributes:
    id (str): Unique identifier for the recipe.
    name (str): Name of the recipe.
    portions (float): Number of portions the recipe yields.
    ingredients (List[Ingredient]): List of ingredients required for the recipe.
        Stored in the DB as a JSON stringified array

Methods:
    reunit(target_unit: Unit):
        Converts all ingredients' units to the specified target unit.
        Raises ValueError if the target unit is not an instance of Unit.

    reportion(target_portions: float):
        Adjusts ingredient quantities proportionally to match the target number of portions.
        Raises ValueError if the target portions is zero or negative.
"""
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
