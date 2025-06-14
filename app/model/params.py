from typing import TypeVar, Optional
from pydantic import BaseModel
from enum import Enum


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
    
