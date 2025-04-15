from sqlalchemy.orm import sessionmaker
from models import User, Ticker, Price
from sqlalchemy import create_engine
from datetime import date

engine = create_engine('sqlite:///portfolio.db')
Session = sessionmaker(bind=engine)
session = Session()

# Create user
user = User(username="testuser")
session.add(user)
session.commit()

# Create ticker
ticker = Ticker(symbol="TEST", user_id=user.id)
session.add(ticker)
session.commit()

# Add price data
price1 = Price(ticker_id=ticker.id, date=date(2025, 4, 5), open=245.0, high=250.0, low=243.0, close=247.0, volume=12345678)
price2 = Price(ticker_id=ticker.id, date=date(2025, 4, 6), open=247.0, high=255.0, low=246.0, close=250.0, volume=9876543)

session.add_all([price1, price2])
session.commit()
