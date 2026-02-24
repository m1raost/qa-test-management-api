from datetime import datetime

from pydantic import BaseModel


class TestSuiteCreate(BaseModel):
    name: str
    description: str | None = None


class TestSuiteUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class TestSuiteRead(BaseModel):
    id: int
    name: str
    description: str | None
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
