from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.test_case import create_case, delete_case, get_case, get_cases_by_suite, update_case
from app.crud.test_suite import get_suite
from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.test_case import TestCaseCreate, TestCaseRead, TestCaseUpdate

router = APIRouter(prefix="/test-cases", tags=["Test Cases"])


def _assert_suite_access(db: Session, suite_id: int, user: User):
    suite = get_suite(db, suite_id)
    if not suite or suite.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Test suite not found")
    return suite


@router.get("/", response_model=list[TestCaseRead])
def list_cases(
    suite_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _assert_suite_access(db, suite_id, current_user)
    return get_cases_by_suite(db, suite_id=suite_id, skip=skip, limit=limit)


@router.post("/", response_model=TestCaseRead, status_code=status.HTTP_201_CREATED)
def create_case_route(
    case_in: TestCaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _assert_suite_access(db, case_in.suite_id, current_user)
    return create_case(db, case_in=case_in)


@router.get("/{case_id}", response_model=TestCaseRead)
def get_case_route(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    case = get_case(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Test case not found")
    _assert_suite_access(db, case.suite_id, current_user)
    return case


@router.patch("/{case_id}", response_model=TestCaseRead)
def update_case_route(
    case_id: int,
    case_in: TestCaseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    case = get_case(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Test case not found")
    _assert_suite_access(db, case.suite_id, current_user)
    return update_case(db, case=case, case_in=case_in)


@router.delete("/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_case_route(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    case = get_case(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Test case not found")
    _assert_suite_access(db, case.suite_id, current_user)
    delete_case(db, case_id=case_id)
