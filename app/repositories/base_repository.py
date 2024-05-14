from sqlalchemy.orm import Session
from typing import Type, TypeVar, List, Optional

# Create a generic repository class
ModelType = TypeVar("ModelType")


class BaseRepository:
    def __init__(self, session: Session, model_type: Type[ModelType]):
        self.session = session
        self.model_type = model_type

    def get(self, id: int) -> Optional[ModelType]:
        return (
            self.session.query(self.model_type).filter(self.model_type.id == id).first()
        )

    def get_multi(self, skip: int = 0, limit: int = 10) -> List[ModelType]:
        return self.session.query(self.model_type).offset(skip).limit(limit).all()

    def create(self, obj_in: dict) -> ModelType:
        obj = self.model_type(**obj_in)
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def update(self, db_obj: ModelType, obj_in: dict) -> ModelType:
        for key, value in obj_in.items():
            setattr(db_obj, key, value)
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def delete(self, db_obj: ModelType) -> None:
        self.session.delete(db_obj)
        self.session.commit()
