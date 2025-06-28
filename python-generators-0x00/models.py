from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column
from sqlalchemy.dialects.mysql import DECIMAL, CHAR
from sqlalchemy import String, text
import uuid


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'user_data'

    user_id = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = mapped_column(String(50), nullable=False)
    email = mapped_column(String(100), nullable=False)
    age = mapped_column(DECIMAL, nullable=False)