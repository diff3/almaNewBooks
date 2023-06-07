from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Almanewbooks(Base):
    __tablename__ = 'almanewbooks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    author = Column(String)
    ddc = Column(String)
    isbn = Column(String)
    released = Column(String)
    title = Column(String)
    date_added = Column(DateTime)

    def __repr__(self):
        return f"<Almanewbooks(id={self.id}, title='{self.title}')>"
