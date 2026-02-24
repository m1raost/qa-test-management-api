from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserRead


class CRUDUser(CRUDBase[User, UserCreate, UserRead]):
    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate, **extra) -> User:  # type: ignore[override]
        db_obj = User(
            email=obj_in.email,
            hashed_password=hash_password(obj_in.password),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(self, db: Session, *, email: str, password: str) -> User | None:
        user = self.get_by_email(db, email)
        if user and verify_password(password, user.hashed_password):
            return user
        return None


crud_user = CRUDUser(User)
