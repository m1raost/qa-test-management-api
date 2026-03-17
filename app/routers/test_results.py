from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.test_result import create_result, delete_result, get_result, get_results_by_run, update_result
from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.test_result import TestResultCreate, TestResultRead, TestResultUpdate

router = APIRouter(prefix="/test-results", tags=["Test Results"])


@router.get("/", response_model=list[TestResultRead])
def list_results(
    run_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return get_results_by_run(db, run_id=run_id, skip=skip, limit=limit)


@router.post("/", response_model=TestResultRead, status_code=status.HTTP_201_CREATED)
def create_result_route(
    result_in: TestResultCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return create_result(db, result_in=result_in)


@router.get("/{result_id}", response_model=TestResultRead)
def get_result_route(
    result_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    result = get_result(db, result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Test result not found")
    return result


@router.patch("/{result_id}", response_model=TestResultRead)
def update_result_route(
    result_id: int,
    result_in: TestResultUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    result = get_result(db, result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Test result not found")
    return update_result(db, result=result, result_in=result_in)


@router.delete("/{result_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_result_route(
    result_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    if not delete_result(db, result_id=result_id):
        raise HTTPException(status_code=404, detail="Test result not found")
