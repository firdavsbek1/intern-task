from sqlalchemy import String,Integer,Column,Boolean
from database import Base


class User(Base):
    __tablename__ = 'users'
    id=Column(Integer,primary_key=True)
    username=Column(String(50),unique=True)
    email=Column(String(250),unique=True)
    password=Column(String(127),nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"user-{self.username}"

