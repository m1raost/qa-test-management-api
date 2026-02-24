from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Generic CRUD operations reused by every resource.
    Subclasses only need to override methods that require custom logic.
    """

    def __init__(self, model: type[ModelType]) -> None:
        self.model = model

    def get(self, db: Session, id: int) -> ModelType | None:
        return db.get(self.model, id)

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> list[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType, **extra: Any) -> ModelType:
        data = obj_in.model_dump()
        data.update(extra)          # inject server-side fields (e.g. owner_id, hashed_password)
        db_obj = self.model(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        changes = obj_in.model_dump(exclude_unset=True)   # only fields the caller provided
        for field, value in changes.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> ModelType | None:
        obj = db.get(self.model, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj
