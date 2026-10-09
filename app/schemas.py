from pydantic import BaseModel, Field


class CreateAdRequest(BaseModel):
    title: str
    description: str
    price: float = Field(..., gt=0)
    author: str


class UpdateAdRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = Field(None, gt=0)
    author: str | None = None
