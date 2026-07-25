from fastapi import FastAPI
from database import SessionLocal
from models import Stock
import yfinance as yf
from pydantic import BaseModel

app = FastAPI(title="FinPulse API")


# Home endpoint
@app.get("/")
def home():
    return {"message": "Welcome to FinPulse API"}


# Get all stocks
@app.get("/stocks")
def get_all_stocks():
    db = SessionLocal()

    stocks = db.query(Stock).all()

    result = []

    for stock in stocks:
        result.append({
            "ticker": stock.ticker,
            "company": stock.company,
            "price": stock.price,
            "market_cap": stock.market_cap,
            "pe_ratio": stock.pe_ratio,
            "eps": stock.eps
        })

    db.close()

    return result


@app.get("/stocks/{ticker}")
def get_stock(ticker: str):

    db = SessionLocal()

    ticker = ticker.upper()

    stock = db.query(Stock).filter(Stock.ticker == ticker).first()

    db.close()

    if stock is None:
        return {"error": "Company not found"}

    return {
        "ticker": stock.ticker,
        "company": stock.company,
        "price": stock.price,
        "market_cap": stock.market_cap,
        "pe_ratio": stock.pe_ratio,
        "eps": stock.eps
    }


# Market Summary
@app.get("/market-summary")
def market_summary():

    db = SessionLocal()

    stocks = db.query(Stock).all()

    total = len(stocks)

    avg_pe = sum(
        stock.pe_ratio for stock in stocks if stock.pe_ratio
    ) / total

    highest = max(stocks, key=lambda x: x.market_cap)

    db.close()

    return {
        "total_companies": total,
        "average_pe": round(avg_pe, 2),
        "highest_market_cap": highest.company
    }


# Historical prices
@app.get("/history/{ticker}")
def history(ticker: str):

    stock = yf.Ticker(ticker)

    history = stock.history(period="6mo")

    data = []

    for date, row in history.iterrows():
        data.append({
            
    "date": str(date.date()),
    "open": float(row["Open"]),
    "high": float(row["High"]),
    "low": float(row["Low"]),
    "close": float(row["Close"]),
    "volume": int(row["Volume"])

        })

    return data
class StockRequest(BaseModel):
    ticker: str
@app.post("/stocks")
def add_stock(stock: StockRequest):

    db = SessionLocal()

    ticker = stock.ticker.upper()

    # Check if already exists
    existing = db.query(Stock).filter(Stock.ticker == ticker).first()

    if existing:
        db.close()
        return {"message": "Stock already exists"}

    try:
        yf_stock = yf.Ticker(ticker)
        info = yf_stock.info

        # Invalid ticker
        if not info or "longName" not in info:
            db.close()
            return {"error": "Company not found"}

        new_stock = Stock(
            ticker=ticker,
            company=info.get("longName"),
            price=info.get("currentPrice", 0),
            market_cap=info.get("marketCap", 0),
            pe_ratio=info.get("trailingPE", 0),
            eps=info.get("trailingEps", 0)
        )

        db.add(new_stock)
        db.commit()

        db.close()

        return {"message": "Stock added successfully"}

    except Exception:
        db.close()
        return {"error": "Company not found"}
@app.delete("/stocks/{ticker}")
def delete_stock(ticker: str):

    db = SessionLocal()

    ticker = ticker.upper()

    stock = db.query(Stock).filter(Stock.ticker == ticker).first()

    if stock is None:
        db.close()
        return {"message": "Company not found"}

    db.delete(stock)
    db.commit()

    db.close()

    return {"message": "Stock deleted successfully"}

