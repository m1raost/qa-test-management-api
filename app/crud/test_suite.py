from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.test_suite import TestSuite
from app.schemas.test_suite import TestSuiteCreate, TestSuiteUpdate


class CRUDTestSuite(CRUDBase[TestSuite, TestSuiteCreate, TestSuiteUpdate]):
    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> list[TestSuite]:
        return (
            db.query(TestSuite)
            .filter(TestSuite.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


crud_test_suite = CRUDTestSuite(TestSuite)
