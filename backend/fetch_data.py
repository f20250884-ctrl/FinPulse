import yfinance as yf

from database import SessionLocal
from models import Stock

# List of 20 Indian stocks
stocks = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "SBIN.NS",
    "ITC.NS",
    "LT.NS",
    "AXISBANK.NS",
    "KOTAKBANK.NS",
    "MARUTI.NS",
    "TITAN.NS",
    "NTPC.NS",
    "POWERGRID.NS",
    "HINDUNILVR.NS",
    "ASIANPAINT.NS",
    "ULTRACEMCO.NS",
    "BAJFINANCE.NS",
    "BHARTIARTL.NS",
    "SUNPHARMA.NS"
]

db = SessionLocal()

for ticker in stocks:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Check if stock already exists
        existing = db.query(Stock).filter(Stock.ticker == ticker).first()

        if existing:
            print(f"{ticker} already exists")
            continue

        new_stock = Stock(
            ticker=ticker,
            company=info.get("longName", ticker),
            price=info.get("currentPrice", 0),
            market_cap=info.get("marketCap", 0),
            pe_ratio=info.get("trailingPE", 0),
            eps=info.get("trailingEps", 0)
        )

        db.add(new_stock)
        db.commit()

        print(f"Added {ticker}")

    except Exception as e:
        print(f"Error with {ticker}: {e}")

db.close()

print("Finished!")