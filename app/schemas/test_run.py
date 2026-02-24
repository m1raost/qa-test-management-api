from datetime import datetime

from pydantic import BaseModel

from app.models.test_run import RunStatus


class TestRunCreate(BaseModel):
    name: str
    suite_id: int | None = None


class TestRunUpdate(BaseModel):
    name: str | None = None
    status: RunStatus | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None


class TestRunRead(BaseModel):
    id: int
    name: str
    status: RunStatus
    suite_id: int | None
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
