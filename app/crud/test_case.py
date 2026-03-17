from sqlalchemy.orm import Session

from app.models.test_case import TestCase
from app.schemas.test_case import TestCaseCreate, TestCaseUpdate


def get_case(db: Session, case_id: int) -> TestCase | None:
    return db.get(TestCase, case_id)


def get_cases_by_suite(
    db: Session, suite_id: int, skip: int = 0, limit: int = 100
) -> list[TestCase]:
    return (
        db.query(TestCase)
        .filter(TestCase.suite_id == suite_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_case(db: Session, case_in: TestCaseCreate) -> TestCase:
    case = TestCase(**case_in.model_dump())
    db.add(case)
    db.commit()
    db.refresh(case)
    return case


def update_case(db: Session, case: TestCase, case_in: TestCaseUpdate) -> TestCase:
    for field, value in case_in.model_dump(exclude_unset=True).items():
        setattr(case, field, value)
    db.commit()
    db.refresh(case)
    return case


def delete_case(db: Session, case_id: int) -> TestCase | None:
    case = db.get(TestCase, case_id)
    if case:
        db.delete(case)
        db.commit()
    return case
