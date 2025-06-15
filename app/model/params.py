from typing import TypeVar, Optional
from pydantic import BaseModel
from enum import Enum

from app.model.unit.unit import MassUnit, VolumeUnit

"""
Request and parameter models for recipe and ingredient API endpoints.
"""

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
    field: Optional[str] = None
    order: Optional[SortOrder] = SortOrder.ASC


class FilterOptions(BaseModel):
    queryString: Optional[str] = None


class RecipesRequest(BaseModel):
    desired_portions: Optional[float] = None
    mass_unit: Optional[MassUnit] = None
    volume_unit: Optional[VolumeUnit] = None


class IngredientsRequest(BaseModel):
    recipe_id: str
    desired_portions: Optional[float] = None
    mass_unit: Optional[MassUnit] = None
    volume_unit: Optional[VolumeUnit] = None
