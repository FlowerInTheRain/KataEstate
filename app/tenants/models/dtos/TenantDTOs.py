from typing import List

from pydantic import BaseModel, constr, RootModel

from constants import PositiveInt

class CreateTenant(BaseModel):
    name: constr(min_length=5, max_length=50)
    contact_info: constr(min_length=10, max_length=12)
    lease_term_start: constr(min_length=10, max_length=10)
    lease_term_end: constr(min_length=10, max_length=10)
    rent_paid: constr(min_length=5, max_length=50)
    property_id: PositiveInt

class UpdateTenant(BaseModel):
    id: PositiveInt
    name: constr(min_length=5, max_length=50)
    contact_info: constr(min_length=10, max_length=12)
    lease_term_start: constr(min_length=10, max_length=10)
    lease_term_end: constr(min_length=10, max_length=10)
    rent_paid: constr(min_length=5, max_length=50)
    property_id: PositiveInt

class TenantDTO(BaseModel):
    name: str
    contact_info: str
    lease_term_start: str
    lease_term_end: str
    rent_paid: str
    property_id: PositiveInt

class TenantResponse(RootModel):
    root: List[TenantDTO]

class TenantIdResponse(RootModel):
    root: int
