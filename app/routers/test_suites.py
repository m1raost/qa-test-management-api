from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.test_suite import crud_test_suite
from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.test_suite import TestSuiteCreate, TestSuiteRead, TestSuiteUpdate

router = APIRouter(prefix="/test-suites", tags=["Test Suites"])


@router.get("/", response_model=list[TestSuiteRead])
def list_suites(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud_test_suite.get_multi_by_owner(db, owner_id=current_user.id, skip=skip, limit=limit)


@router.post("/", response_model=TestSuiteRead, status_code=status.HTTP_201_CREATED)
def create_suite(
    suite_in: TestSuiteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud_test_suite.create(db, obj_in=suite_in, owner_id=current_user.id)


@router.get("/{suite_id}", response_model=TestSuiteRead)
def get_suite(
    suite_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    suite = crud_test_suite.get(db, suite_id)
    if not suite or suite.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Test suite not found")
    return suite


@router.patch("/{suite_id}", response_model=TestSuiteRead)
def update_suite(
    suite_id: int,
    suite_in: TestSuiteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    suite = crud_test_suite.get(db, suite_id)
    if not suite or suite.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Test suite not found")
    return crud_test_suite.update(db, db_obj=suite, obj_in=suite_in)


@router.delete("/{suite_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_suite(
    suite_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    suite = crud_test_suite.get(db, suite_id)
    if not suite or suite.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Test suite not found")
    crud_test_suite.delete(db, id=suite_id)
