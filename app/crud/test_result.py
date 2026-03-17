from sqlalchemy.orm import Session

from app.models.test_result import TestResult
from app.schemas.test_result import TestResultCreate, TestResultUpdate


def get_result(db: Session, result_id: int) -> TestResult | None:
    return db.get(TestResult, result_id)


def get_results_by_run(
    db: Session, run_id: int, skip: int = 0, limit: int = 100
) -> list[TestResult]:
    return (
        db.query(TestResult)
        .filter(TestResult.run_id == run_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_result(db: Session, result_in: TestResultCreate) -> TestResult:
    result = TestResult(**result_in.model_dump())
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


def update_result(
    db: Session, result: TestResult, result_in: TestResultUpdate
) -> TestResult:
    for field, value in result_in.model_dump(exclude_unset=True).items():
        setattr(result, field, value)
    db.commit()
    db.refresh(result)
    return result


def delete_result(db: Session, result_id: int) -> TestResult | None:
    result = db.get(TestResult, result_id)
    if result:
        db.delete(result)
        db.commit()
    return result
