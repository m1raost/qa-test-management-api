from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.test_result import TestResult
from app.schemas.test_result import TestResultCreate, TestResultUpdate


class CRUDTestResult(CRUDBase[TestResult, TestResultCreate, TestResultUpdate]):
    def get_multi_by_run(
        self, db: Session, *, run_id: int, skip: int = 0, limit: int = 100
    ) -> list[TestResult]:
        return (
            db.query(TestResult)
            .filter(TestResult.run_id == run_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


crud_test_result = CRUDTestResult(TestResult)
