# 📈 FinPulse - Stock Market Monitoring Platform

## Overview

FinPulse is a web-based stock market monitoring platform developed as part of the AlgoLabs Assignment. It tracks Indian listed companies, stores financial data in a SQLite database, exposes REST APIs using FastAPI, and provides an interactive dashboard built with Streamlit.

The application allows users to monitor live market information, compare companies, analyze historical stock prices, and perform simple portfolio analysis.

---

## Features

### 📊 Market Data
- Track 20+ Indian listed companies
- Live Stock Price
- Market Capitalization
- P/E Ratio
- Earnings Per Share (EPS)
- Historical Price Data

### 📈 Dashboard
- Interactive Line Chart
- Candlestick Chart
- Company Comparison
- Fundamental Metrics
- Search Stocks
- Add New Stocks
- Delete Existing Stocks
- Dark / Light Theme

### 🤖 AI Insights
- Rule-based Stock Analysis
- Portfolio Recommendations
- Basic Investment Insights

### 💼 Portfolio Analysis
- Add multiple stocks
- Enter quantity and purchase price
- Calculate Investment Value
- Profit/Loss
- ROI Percentage
- Portfolio Allocation Pie Chart

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3 |
| Backend | FastAPI |
| Database | SQLite |
| ORM | SQLAlchemy |
| Frontend | Streamlit |
| Charts | Plotly |
| Market Data | Yahoo Finance (yFinance) |
| HTTP Requests | Requests |

---

## Project Structure

```
FinPulse/
│
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── models.py
│   ├── fetch_data.py
│   ├── stocks.db
│   └── requirements.txt
│
├── frontend/
│   ├── dashboard.py
│   └── requirements.txt
│
├── screenshots/
│
├── README.md
└── report.pdf
```

---

## Database Schema

### Stock Table

| Column | Type |
|----------|---------|
| id | Integer |
| ticker | String |
| company | String |
| price | Float |
| market_cap | Float |
| pe_ratio | Float |
| eps | Float |

---

## REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Home Page |
| GET | /stocks | Retrieve all tracked stocks |
| GET | /stocks/{ticker} | Retrieve details of a specific stock |
| GET | /market-summary | Display market summary |
| GET | /history/{ticker} | Retrieve historical stock prices |
| POST | /stocks | Add a new stock |
| DELETE | /stocks/{ticker} | Delete a stock |

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/FinPulse.git
cd FinPulse
```

### Install Dependencies

```bash
pip install -r backend/requirements.txt
```

---

## Running the Backend

```bash
cd backend
uvicorn app:app --reload
```

Open:

```
http://127.0.0.1:8000
```

Swagger API Documentation:

```
http://127.0.0.1:8000/docs
```

---

## Running the Frontend

Open a new terminal.

```bash
cd frontend
streamlit run dashboard.py
```

Dashboard:

```
http://localhost:8501
```

---

## Screenshots

Include screenshots of:

- Dashboard Home
- Historical Price Chart
- Candlestick Chart
- Company Comparison
- Portfolio Analysis
- API Documentation (Swagger)

---

## Challenges Faced

- Integrating live stock market data using yFinance.
- Managing database operations with SQLAlchemy.
- Synchronizing backend APIs with the Streamlit dashboard.
- Designing an intuitive dashboard for financial data visualization.

---

## Future Enhancements

- User Authentication
- Portfolio Persistence
- Watchlist Feature
- Email Alerts
- Telegram Notifications
- Technical Indicators (RSI, MACD, Bollinger Bands)
- Sector-wise Analysis
- AI-powered Stock Recommendation System
- Cloud Database (PostgreSQL / Supabase)
- Real-time Data Updates

---

## APIs Used

- Yahoo Finance (yFinance)

---

## Deployment

### Backend

Deploy using Render or any FastAPI-compatible hosting service.

### Frontend

Deploy using Streamlit Community Cloud.

---

## Author

Developed by **<Your Name>** as part of the **AlgoLabs Assignment – FinPulse**.

---

## License

This project is intended for educational purposes only.