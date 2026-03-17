from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.test_suite import create_suite, delete_suite, get_suite, get_suites_by_owner, update_suite
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
    return get_suites_by_owner(db, owner_id=current_user.id, skip=skip, limit=limit)


@router.post("/", response_model=TestSuiteRead, status_code=status.HTTP_201_CREATED)
def create_suite_route(
    suite_in: TestSuiteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_suite(db, suite_in=suite_in, owner_id=current_user.id)


@router.get("/{suite_id}", response_model=TestSuiteRead)
def get_suite_route(
    suite_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    suite = get_suite(db, suite_id)
    if not suite or suite.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Test suite not found")
    return suite


@router.patch("/{suite_id}", response_model=TestSuiteRead)
def update_suite_route(
    suite_id: int,
    suite_in: TestSuiteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    suite = get_suite(db, suite_id)
    if not suite or suite.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Test suite not found")
    return update_suite(db, suite=suite, suite_in=suite_in)


@router.delete("/{suite_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_suite_route(
    suite_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    suite = get_suite(db, suite_id)
    if not suite or suite.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Test suite not found")
    delete_suite(db, suite_id=suite_id)
