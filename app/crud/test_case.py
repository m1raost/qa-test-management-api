from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.test_case import TestCase
from app.schemas.test_case import TestCaseCreate, TestCaseUpdate


class CRUDTestCase(CRUDBase[TestCase, TestCaseCreate, TestCaseUpdate]):
    def get_multi_by_suite(
        self, db: Session, *, suite_id: int, skip: int = 0, limit: int = 100
    ) -> list[TestCase]:
        return (
            db.query(TestCase)
            .filter(TestCase.suite_id == suite_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


crud_test_case = CRUDTestCase(TestCase)
