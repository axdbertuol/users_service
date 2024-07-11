from ksuid import Ksuid
from sqlalchemy import Column, String

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(27), primary_key=True, default=lambda: Ksuid().__str__())

    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(
        String,
    )
    status = Column(String, default="inactive")
    role = Column(String, default="user")
    social_id = Column(String, default="")

    full_name = Column(String, index=True)
