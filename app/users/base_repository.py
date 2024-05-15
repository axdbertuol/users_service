from fastapi.logger import logger
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import Type, TypeVar, List, Optional

from app.common.exceptions import DuplicatedError, InternalServerError


# Create a generic repository class
ModelType = TypeVar("ModelType")


class BaseRepository:
    def __init__(self, session: Session, model_type: Type[ModelType]):
        self.session = session
        self.model_type = model_type

    def get(self, id: int) -> Optional[ModelType]:
        try:
            result = (
                self.session.query(self.model_type)
                .filter(self.model_type.id == id)
                .first()
            )

            return result
        except (SQLAlchemyError, IntegrityError) as e:
            logger.error(e)
            raise InternalServerError(e.args)

    def get_multi(
        self, skip: int = 0, limit: int = 10
    ) -> Optional[List[Optional[ModelType]]]:
        try:
            result = self.session.query(self.model_type).offset(skip).limit(limit).all()
            return result
        except (SQLAlchemyError, IntegrityError) as e:
            logger.error("Database error: %s", e)
            raise InternalServerError(e.args)

    def create(self, obj_in: dict) -> ModelType:
        try:
            obj = self.model_type(**obj_in)
            self.session.add(obj)
            self.session.commit()
            self.session.refresh(obj)

            return obj
        except IntegrityError as e:
            self.session.rollback()  # Rollback changes in case of error
            if "unique constraint" in str(e):
                logger.error("Duplicated entry: %s", e)
                raise DuplicatedError(e.args)
            else:
                logger.error("Database error: %s", e)
                raise InternalServerError(e.args)
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error("Database error: %s", e)

            raise InternalServerError()

    def update(self, db_obj: ModelType, obj_in: dict) -> None:
        try:
            for key, value in obj_in.items():
                setattr(db_obj, key, value)
            self.session.add(db_obj)
            self.session.commit()
            self.session.refresh(db_obj)
            return None
        except IntegrityError as e:
            self.session.rollback()  # Rollback changes in case of error
            if "unique constraint" in str(e):
                logger.error("Duplicated entry: %s", e)
                raise DuplicatedError(e.args)
            else:
                raise InternalServerError(e.args)
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error("Database error: %s", e)
            raise InternalServerError(e.args)

    def delete(self, db_obj: ModelType) -> None:
        try:
            self.session.delete(db_obj)
            self.session.commit()
            return None
        except (SQLAlchemyError, IntegrityError) as e:
            self.session.rollback()
            logger.error("Database error: %s", e)
            raise InternalServerError(e.args)
