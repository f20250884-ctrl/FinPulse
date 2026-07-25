from sqlalchemy import Column, Integer, String, Float

from database import Base, engine


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, unique=True, index=True)
    company = Column(String)
    price = Column(Float)
    market_cap = Column(Float)
    pe_ratio = Column(Float)
    eps = Column(Float)


# Create the table in SQLite
Base.metadata.create_all(bind=engine)

print("Database and table created successfully!")