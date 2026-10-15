from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, StringConstraints, field_validator

from app.domain.customer import CustomerStatus

CustomerName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=100),
]


class CustomerCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: CustomerName
    email: EmailStr

    @field_validator("email", mode="before")
    @classmethod
    def strip_email(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value


class CustomerStatusUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: CustomerStatus


class CustomerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    status: CustomerStatus
    created_at: datetime
