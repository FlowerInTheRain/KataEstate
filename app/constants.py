from typing import Annotated

from pydantic import Field, RootModel

API_base_path = "/api"
PositiveInt = Annotated[int, Field(gt=0)]

class CreateItemResponse(RootModel):
    root: int
