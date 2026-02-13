from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


# 👩‍💼 Government Employee Table
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    contact_info = Column(String)
    sector = Column(String)
    position = Column(String)

    blogs = relationship("Blog", back_populates="author")


# 📝 Blog Table
class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    author_id = Column(Integer, ForeignKey("employees.id"))
    author = relationship("Employee", back_populates="blogs")

    comments = relationship("Comment", back_populates="blog")


# 💬 Comment Table (Public users)
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    text = Column(Text)

    blog_id = Column(Integer, ForeignKey("blogs.id"))
    blog = relationship("Blog", back_populates="comments")
