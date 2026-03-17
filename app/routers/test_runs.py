from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.test_run import create_run, delete_run, get_run, get_runs, update_run
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
    return get_runs(db, skip=skip, limit=limit)


@router.post("/", response_model=TestRunRead, status_code=status.HTTP_201_CREATED)
def create_run_route(
    run_in: TestRunCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return create_run(db, run_in=run_in)


@router.get("/{run_id}", response_model=TestRunRead)
def get_run_route(
    run_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    run = get_run(db, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Test run not found")
    return run


@router.patch("/{run_id}", response_model=TestRunRead)
def update_run_route(
    run_id: int,
    run_in: TestRunUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    run = get_run(db, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Test run not found")
    return update_run(db, run=run, run_in=run_in)


@router.delete("/{run_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_run_route(
    run_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    if not delete_run(db, run_id=run_id):
        raise HTTPException(status_code=404, detail="Test run not found")
