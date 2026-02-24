from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.test_run import crud_test_run
from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.test_run import TestRunCreate, TestRunRead, TestRunUpdate

router = APIRouter(prefix="/test-runs", tags=["Test Runs"])


@router.get("/", response_model=list[TestRunRead])
def list_runs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return crud_test_run.get_multi(db, skip=skip, limit=limit)


@router.post("/", response_model=TestRunRead, status_code=status.HTTP_201_CREATED)
def create_run(
    run_in: TestRunCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return crud_test_run.create(db, obj_in=run_in)


@router.get("/{run_id}", response_model=TestRunRead)
def get_run(
    run_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    run = crud_test_run.get(db, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Test run not found")
    return run


@router.patch("/{run_id}", response_model=TestRunRead)
def update_run(
    run_id: int,
    run_in: TestRunUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    run = crud_test_run.get(db, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Test run not found")
    return crud_test_run.update(db, db_obj=run, obj_in=run_in)


@router.delete("/{run_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_run(
    run_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    if not crud_test_run.delete(db, id=run_id):
        raise HTTPException(status_code=404, detail="Test run not found")
