from fastapi.logger import logger
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import Dict, Type, TypeVar, List, Optional

from app.dtos.responses import ResponseModel

# Create a generic repository class
ModelType = TypeVar("ModelType")


class BaseRepository:
    def __init__(self, session: Session, model_type: Type[ModelType]):
        self.session = session
        self.model_type = model_type

    def get(self, id: int) -> Optional[Dict[str, Optional[ModelType]]]:
        try:
            result = (
                self.session.query(self.model_type)
                .filter(self.model_type.id == id)
                .first()
            )
            response_success = ResponseModel[Dict[str, Optional[ModelType]]](
                success=True, data=result
            )

            return response_success
        except SQLAlchemyError as e:
            logger.error(e)
            response_failure = ResponseModel(success=False, error="Database error")
            return response_failure

    def get_multi(
        self, skip: int = 0, limit: int = 10
    ) -> ResponseModel[List[Dict[str, Optional[ModelType]]]]:
        try:
            result = self.session.query(self.model_type).offset(skip).limit(limit).all()
            response_success = ResponseModel[List[Dict[str, Optional[ModelType]]]](
                success=True, data=result
            )
            return response_success
        except SQLAlchemyError as e:
            logger.error("Database error: %s", e)
            response_failure = ResponseModel(success=False, error="Database error")
            return response_failure

    def create(self, obj_in: dict) -> ResponseModel[Dict[str, Optional[ModelType]]]:
        try:
            obj = self.model_type(**obj_in)
            self.session.add(obj)
            self.session.commit()
            self.session.refresh(obj)

            response_success = ResponseModel[Dict[str, Optional[ModelType]]](
                success=True, data=obj
            )

            return response_success
        except IntegrityError as e:
            self.session.rollback()  # Rollback changes in case of error
            if "unique constraint" in str(e):
                logger.error("Duplicated entry: %s", e)
                response_failure = ResponseModel(
                    success=False, error="Duplicated entry"
                )
                return response_failure
            else:
                logger.error("Database error: %s", e)
                response_failure = ResponseModel(success=False, error="Database error")
                return response_failure
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error("Database error: %s", e)
            response_failure = ResponseModel(success=False, error="Database error")
            return response_failure

    def update(self, db_obj: ModelType, obj_in: dict) -> ResponseModel:
        try:
            for key, value in obj_in.items():
                setattr(db_obj, key, value)
            self.session.add(db_obj)
            self.session.commit()
            self.session.refresh(db_obj)
            response_success = ResponseModel(success=True)
            return response_success
        except IntegrityError as e:
            self.session.rollback()  # Rollback changes in case of error
            if "unique constraint" in str(e):
                logger.error("Duplicated entry: %s", e)
                response_failure = ResponseModel(
                    success=False, error="Duplicated entry"
                )
                return response_failure
            else:
                logger.error("Database error: %s", e)
                response_failure = ResponseModel(success=False, error="Database error")
                return response_failure
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error("Database error: %s", e)
            return response_failure

    def delete(self, db_obj: ModelType) -> ResponseModel:
        try:
            self.session.delete(db_obj)
            self.session.commit()
            response_success = ResponseModel(success=True)
            return response_success
        except IntegrityError as e:
            self.session.rollback()
            logger.error("Database error: %s", e)
            response_failure = ResponseModel(success=False, error="Database error")
            return response_failure
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error("Database error: %s", e)
            response_failure = ResponseModel(success=False, error="Database error")
            return response_failure
