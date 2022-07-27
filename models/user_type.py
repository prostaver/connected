from sqlalchemy import Column, String, Integer

from config.database import Base

class UserType(Base):
    __tablename__ = "user_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), nullable=False)

    def __repr__(self):
        return f"<UserType id = {self.id}, name = {self.name}>"
