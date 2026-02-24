from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.test_run import TestRun
from app.schemas.test_run import TestRunCreate, TestRunUpdate


class CRUDTestRun(CRUDBase[TestRun, TestRunCreate, TestRunUpdate]):
    def get_multi_by_suite(
        self, db: Session, *, suite_id: int, skip: int = 0, limit: int = 100
    ) -> list[TestRun]:
        return (
            db.query(TestRun)
            .filter(TestRun.suite_id == suite_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


crud_test_run = CRUDTestRun(TestRun)
