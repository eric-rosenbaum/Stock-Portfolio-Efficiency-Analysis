import sqlite3
import pandas as pd
import requests
import time
import os
import sys
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import streamlit as st

# Step 1: Fix import path for models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from data.models import Ticker, Price  # assuming User isn't used yet

# Step 2: Config
ALPHA_VANTAGE_API_KEY = st.secrets["ALPHA_VANTAGE_API_KEY"]
BASE_URL = "https://www.alphavantage.co/query"
DATABASE_URL = 'sqlite:///portfolio.db'

# Step 3: Set up SQLAlchemy session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# ------------------------------
# Step 4: Fetch and store data
# ------------------------------
def fetch_data(symbol):
    session = Session()

    print(f"Fetching data for {symbol} from Alpha Vantage...")

    url = f'{BASE_URL}?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={ALPHA_VANTAGE_API_KEY}'
    r = requests.get(url)
    data = r.json()

    # Debug: Check response
    if 'Time Series (Daily)' not in data:
        print("❌ API Error or rate limit hit:")
        print(data)
        session.close()
        return None

    daily_data = data['Time Series (Daily)']
    df = pd.DataFrame.from_dict(daily_data, orient='index').reset_index()
    df = df.rename(columns={
        'index': 'date',
        '1. open': 'open',
        '2. high': 'high',
        '3. low': 'low',
        '4. close': 'close',
        '5. volume': 'volume'
    })

    df['date'] = pd.to_datetime(df['date'])
    df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']].astype(float)
    df['volume'] = df['volume'].astype(int)

    # Debug: Check dataframe
    print(f"✅ Fetched {len(df)} rows for {symbol}")
    print(df.head(2))

    # Step 5: Insert ticker if not in DB
    existing_ticker = session.query(Ticker).filter_by(symbol=symbol).first()
    if not existing_ticker:
        print(f"ℹ️ Ticker {symbol} not in DB. Creating new entry.")
        existing_ticker = Ticker(symbol=symbol)
        session.add(existing_ticker)
        session.commit()
    else:
        print(f"✅ Ticker {symbol} already exists in DB (id={existing_ticker.id})")

    # Step 6: Insert price data
    inserted_rows = 0
    for _, row in df.iterrows():
        existing_price = session.query(Price).filter_by(ticker_id=existing_ticker.id, date=row['date']).first()
        if not existing_price:
            price = Price(
                ticker_id=existing_ticker.id,
                date=row['date'],
                open=row['open'],
                high=row['high'],
                low=row['low'],
                close=row['close'],
                volume=row['volume']
            )
            session.add(price)
            inserted_rows += 1

    session.commit()
    session.close()

    print(f"✅ Inserted {inserted_rows} new price records for {symbol}")
    return df


# ------------------------------
# Step 7: Read from DB
# ------------------------------
def get_ticker_prices(symbol):
    session = Session()

    ticker = session.query(Ticker).filter_by(symbol=symbol).first()
    if not ticker:
        print(f"❌ No ticker found in DB with symbol '{symbol}'")
        session.close()
        return []

    prices = session.query(Price).filter_by(ticker_id=ticker.id).order_by(Price.date).all()

    if not prices:
        print(f"❌ No price data found for ticker {symbol}")
        session.close()
        return []

    result = [{
        'date': price.date,
        'open': price.open,
        'high': price.high,
        'low': price.low,
        'close': price.close,
        'volume': price.volume
    } for price in prices]

    session.close()
    print(f"✅ Retrieved {len(result)} records for {symbol}")
    return result


# ------------------------------
# Step 8: Main flow
# ------------------------------
if __name__ == '__main__':
    TICKER = 'AAPL'

    # OPTIONAL: Only fetch if not already in DB
    data_in_db = get_ticker_prices(TICKER)
    if not data_in_db:
        fetch_data(TICKER)

    # Get from DB
    data = get_ticker_prices(TICKER)
    print("📊 First 5 rows from DB:")
    for row in data[:5]:
        print(row)
