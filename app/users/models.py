from sqlalchemy import Column, Integer, String
from app.common.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    status = Column(String, default="inactive")
    role = Column(String, default="user")
    social_id = Column(String, default="")

    full_name = Column(String, index=True)
    # items = relationship("Item", back_populates="owner")
