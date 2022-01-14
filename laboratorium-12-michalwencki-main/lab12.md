from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

db_string = "postgres://user:password@ip_adrress:port/db_name"

engine = create_engine(db_string)

Base = declarative_base()

'''class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    surname = Column(String(50))
    born_date = Column(Date)

    def __repr__(self):
        return "<authors(id='{0}', name={1}, surname={2}, born_date={3})>".format(
            self.id, self.name, self.surnamey, self.born_date)'''
