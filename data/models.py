from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

# Users Table
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)

    tickers = relationship('Ticker', back_populates='user')

# Tickers Table
class Ticker(Base):
    __tablename__ = 'tickers'
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='tickers')
    prices = relationship('Price', back_populates='ticker')

# Prices Table
class Price(Base):
    __tablename__ = 'prices'
    id = Column(Integer, primary_key=True)
    ticker_id = Column(Integer, ForeignKey('tickers.id'))
    date = Column(Date)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)

    ticker = relationship('Ticker', back_populates='prices')
