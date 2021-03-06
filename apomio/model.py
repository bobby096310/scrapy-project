from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, Float)
from scrapy.utils.project import get_project_settings

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    Base.metadata.create_all(engine)


class Offer(Base):
    __tablename__ = "offer"

    pzn = Column(Integer, primary_key=True)
    product = Column('product', String(50))
    provider = Column('provider', String(100), primary_key=True)
    rate = Column('rate', Float)
    reviews = Column('reviews', Integer)
    payment = Column('payment', String(200))
    delivery = Column('delivery', String(300))
    price = Column('price', Float)
    total_price = Column('total_price', Float)