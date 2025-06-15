from typing import TypeVar, Optional
from pydantic import BaseModel
from enum import Enum

from app.model.ingredient.ingredient import Unit


T = TypeVar("T")


class PaginationParams(BaseModel):
    page: int = 1
    size: int = 5

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class SortOptions(BaseModel):
    field: str
    order: SortOrder = SortOrder.ASC


class FilterOptions(BaseModel):
    queryString: Optional[str] = None


class RecipesRequest(BaseModel):
    desired_portions: Optional[float] = None
    mass_unit: Optional[Unit] = None
    volume_unit: Optional[Unit] = None


class IngredientsRequest(BaseModel):
    recipe_id: str
    desired_portions: Optional[float] = None
    mass_unit: Optional[Unit] = None
    volume_unit: Optional[Unit] = None
