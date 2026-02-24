from datetime import datetime

from pydantic import BaseModel

from app.models.test_case import CaseStatus, Priority, Severity


class TestCaseCreate(BaseModel):
    title: str
    description: str | None = None
    steps: str | None = None
    expected_result: str | None = None
    priority: Priority = Priority.medium
    severity: Severity = Severity.major
    status: CaseStatus = CaseStatus.draft
    suite_id: int


class TestCaseUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    steps: str | None = None
    expected_result: str | None = None
    priority: Priority | None = None
    severity: Severity | None = None
    status: CaseStatus | None = None


class TestCaseRead(BaseModel):
    id: int
    title: str
    description: str | None
    steps: str | None
    expected_result: str | None
    priority: Priority
    severity: Severity
    status: CaseStatus
    suite_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
