from typing import List
from pydantic import BaseModel
from app.model.ingredient.ingredient import Ingredient


class Recipe(BaseModel):
    id: str
    name: str
    portions: float
    ingredients: List[Ingredient]

    def reportion(self, target_portions: float) -> "Recipe":
        if target_portions <= 0:
            raise ValueError("Target portions must be greater than zero.")
            
        multiplier = target_portions / self.portions
        for ingredient in self.ingredients:
            ingredient.reportion(multiplier)
        
        self.portions = target_portions
