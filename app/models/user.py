from app.db.database import Base
from sqlalchemy import Column, Integer, Boolean, Text, String


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(100), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)

    def __repr__(self):
        return f"<user: {self.username}>"

    @staticmethod
    def get_by_username(session, username):
        db_username = session.query(User).filter(User.username == username).first()
        return db_username

    @staticmethod
    def get_by_email(session, email):
        db_username = session.query(User).filter(User.username == email).first()
        return db_username
