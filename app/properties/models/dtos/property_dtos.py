from typing import List

from pydantic import BaseModel, constr, RootModel

from properties.models.PropertyStatuses import PropertyStatuses
from properties.models.PropertyTypes import PropertyTypes


class PropertyRequest(BaseModel):
    id: int
    address: constr(min_length=10, max_length=250)
    type: str
    status: str
    purchase_date: str
    price: int

class PropertyDTO(BaseModel):
    id: int
    address: str
    type: str
    status: str
    purchase_date: str
    price: int

class PropertyResponse(RootModel):
    root: List[PropertyDTO]


class CreatePropertyResponse(RootModel):
    root: int

class AddPropertyRequest(BaseModel):
    id: int
    address: str
    type: PropertyTypes
    status: PropertyStatuses
    purchase_date: str
    price: str