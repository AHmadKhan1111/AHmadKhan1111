from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict


class BirdBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    species: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., ge=0)
    in_stock: int = Field(..., ge=0)
    description: Optional[str] = None


class BirdCreate(BirdBase):
    pass


class BirdUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    species: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[float] = Field(None, ge=0)
    in_stock: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None


class BirdOut(BirdBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BirdListResponse(BaseModel):
    items: List[BirdOut]
    total: int