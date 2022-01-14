from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DATE, VARCHAR, Float
from sqlalchemy.sql.type_api import INTEGERTYPE

db_string = "postgres://user:password@localhost/db_name"

engine = create_engine(db_string)

Base = declarative_base()

class Country(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    country_code = Column(String(50))
    def __repr__(self):
        return "<countries(id='{0}', name={1}, country_code={2})>".format(
            self.id, self.name, self.country_code)

class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey('countries.id'))
    name = Column(String(50))
    def __repr__(self):
        return "<cities(id='{0}', name={1}, country_id={2})>".format(
            self.id, self.name, self.country_id)

class Place(Base):
    __tablename__ = 'places'
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('cities.id'))
    host_id = Column(Integer, ForeignKey('hosts.id'))
    address = Column(String(50))
    def __repr__(self):
        return "<places(id='{0}', city_id={1}, host_id={2}, address={3})>".format(
            self.id, self.city_id, self.host_id, self.address)

class Host(Base):
    __tablename__ = 'hosts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    def __repr__(self):
        return "<hosts(id='{0}', user_id={1}>".format(
            self.id, self.user_id)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(50))
    def __repr__(self):
        return "<users(id='{0}', email={1})>".format(
            self.id, self.email)

class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    place_id = Column(Integer, ForeignKey('places.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    price_per_night = Column(Float)
    num_nights = Column(Integer)
    def __repr__(self):
        return "<bookings(id='{0}', user_id={1}, place_id={2}, start_date={3}, end_date={4}, price_per_night={5}, num_nights={6})>".format(
            self.id, self.user_id, self.place_id, self.start_date, self.end_date, self.price_per_night, self.num_nights)
    
class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey('bookings.id'))
    rating = Column(Integer)
    def __repr__(self):
        return "<reviews(id='{0}', booking_id={1}, rating={2})>".format(
            self.id, self.booking_id, self.rating)

Base.metadata.create_all(engine)