from sqlalchemy.orm import Session

from app.models.test_run import TestRun
from app.schemas.test_run import TestRunCreate, TestRunUpdate


def get_run(db: Session, run_id: int) -> TestRun | None:
    return db.get(TestRun, run_id)


def get_runs(db: Session, skip: int = 0, limit: int = 100) -> list[TestRun]:
    return db.query(TestRun).offset(skip).limit(limit).all()


def create_run(db: Session, run_in: TestRunCreate) -> TestRun:
    run = TestRun(**run_in.model_dump())
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def update_run(db: Session, run: TestRun, run_in: TestRunUpdate) -> TestRun:
    for field, value in run_in.model_dump(exclude_unset=True).items():
        setattr(run, field, value)
    db.commit()
    db.refresh(run)
    return run


def delete_run(db: Session, run_id: int) -> TestRun | None:
    run = db.get(TestRun, run_id)
    if run:
        db.delete(run)
        db.commit()
    return run
