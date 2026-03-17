from sqlalchemy.orm import Session

from app.models.test_suite import TestSuite
from app.schemas.test_suite import TestSuiteCreate, TestSuiteUpdate


def get_suite(db: Session, suite_id: int) -> TestSuite | None:
    return db.get(TestSuite, suite_id)


def get_suites_by_owner(
    db: Session, owner_id: int, skip: int = 0, limit: int = 100
) -> list[TestSuite]:
    return (
        db.query(TestSuite)
        .filter(TestSuite.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_suite(db: Session, suite_in: TestSuiteCreate, owner_id: int) -> TestSuite:
    suite = TestSuite(**suite_in.model_dump(), owner_id=owner_id)
    db.add(suite)
    db.commit()
    db.refresh(suite)
    return suite


def update_suite(db: Session, suite: TestSuite, suite_in: TestSuiteUpdate) -> TestSuite:
    for field, value in suite_in.model_dump(exclude_unset=True).items():
        setattr(suite, field, value)
    db.commit()
    db.refresh(suite)
    return suite


def delete_suite(db: Session, suite_id: int) -> TestSuite | None:
    suite = db.get(TestSuite, suite_id)
    if suite:
        db.delete(suite)
        db.commit()
    return suite
