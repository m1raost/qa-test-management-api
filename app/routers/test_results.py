from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.test_result import crud_test_result
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
    return crud_test_result.get_multi_by_run(db, run_id=run_id, skip=skip, limit=limit)


@router.post("/", response_model=TestResultRead, status_code=status.HTTP_201_CREATED)
def create_result(
    result_in: TestResultCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return crud_test_result.create(db, obj_in=result_in)


@router.get("/{result_id}", response_model=TestResultRead)
def get_result(
    result_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    result = crud_test_result.get(db, result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Test result not found")
    return result


@router.patch("/{result_id}", response_model=TestResultRead)
def update_result(
    result_id: int,
    result_in: TestResultUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    result = crud_test_result.get(db, result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Test result not found")
    return crud_test_result.update(db, db_obj=result, obj_in=result_in)


@router.delete("/{result_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_result(
    result_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    if not crud_test_result.delete(db, id=result_id):
        raise HTTPException(status_code=404, detail="Test result not found")
