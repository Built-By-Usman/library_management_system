from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    books = relationship("BookModel", back_populates="owner")

class BookModel(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    author = Column(String)
    category = Column(String)
    ISBN = Column(String)
    copies = Column(Integer)
    url = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("UserModel", back_populates="books")

class IssueReturnModel(Base):
    __tablename__ = "IssueReturn"
    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    student_id = Column(Integer, nullable=False)

    status = Column(String, default="issued")
    issue_days = Column(Integer, nullable=False)
    borrow_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=True)

    user = relationship("UserModel")
    book = relationship("BookModel")