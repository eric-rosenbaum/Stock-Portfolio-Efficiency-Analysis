from sqlalchemy import create_engine
from models import Base

# Create a new SQLite DB file (or connect if it exists)
engine = create_engine('sqlite:///portfolio.db')

# Create all tables defined in models.py
Base.metadata.create_all(engine)
