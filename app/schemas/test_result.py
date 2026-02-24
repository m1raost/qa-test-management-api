from datetime import datetime

from pydantic import BaseModel

from app.models.test_result import ResultStatus


class TestResultCreate(BaseModel):
    run_id: int
    test_case_id: int
    status: ResultStatus
    notes: str | None = None
    duration_ms: int | None = None


class TestResultUpdate(BaseModel):
    status: ResultStatus | None = None
    notes: str | None = None
    duration_ms: int | None = None


class TestResultRead(BaseModel):
    id: int
    run_id: int
    test_case_id: int
    status: ResultStatus
    notes: str | None
    duration_ms: int | None
    executed_at: datetime

    model_config = {"from_attributes": True}
