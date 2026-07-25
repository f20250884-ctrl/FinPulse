import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
def ai_summary(stock):

    text = ""

    if stock["pe_ratio"] > 35:
        text += "• Stock appears relatively expensive based on P/E ratio.\n"

    elif stock["pe_ratio"] > 0:
        text += "• P/E ratio is within a reasonable range.\n"

    if stock["eps"] > 50:
        text += "• Company has strong earnings per share.\n"

    if stock["market_cap"] > 1_000_000_000_000:
        text += "• Large-cap company with significant market value.\n"

    if stock["price"] > 2000:
        text += "• Trading at a premium price.\n"

    return text

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="FinPulse", layout="wide")

st.title("📈 FinPulse - Indian Stock Dashboard")
st.markdown("""
Monitor Indian stocks with live market data,
fundamental metrics, and historical price charts.
""")
theme = st.sidebar.radio(
    "Theme",
    ["Light", "Dark"]
)

if theme == "Dark":
    st.markdown("""
        <style>
        .stApp{
            background-color:#0E1117;
            color:white;
        }
        </style>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
        <style>
        .stApp{
            background-color:white;
            color:black;
        }
        </style>
    """, unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.header("📊 Stock Management")

stock_input = st.sidebar.text_input(
    "Enter Stock Ticker",
    placeholder="Example: WIPRO.NS"
)

col1, col2, col3 = st.sidebar.columns(3)

search = col1.button("🔍 Search")
add = col2.button("➕ Add")
delete = col3.button("🗑 Delete")
if search:

    if stock_input.strip() == "":
        st.sidebar.warning("Please enter a ticker.")

    else:

        response = requests.get(
            f"{API_URL}/stocks/{stock_input.upper()}"
        )

        data = response.json()

        if "error" in data:

            st.sidebar.error("❌ Company not found")

        else:

            st.sidebar.success("✅ Company Found")

            st.sidebar.write(f"**{data['company']}**")
            st.sidebar.write(f"Price: ₹{data['price']}")
            st.sidebar.write(f"P/E Ratio: {data['pe_ratio']}")
            st.sidebar.write(f"EPS: {data['eps']}")
if add:

    if stock_input.strip() == "":
        st.sidebar.warning("Please enter a ticker.")

    else:

        response = requests.post(
            f"{API_URL}/stocks",
            json={
                "ticker": stock_input.upper()
            }
        )

        data = response.json()

        if "error" in data:

            st.sidebar.error("❌ Company not found")

        elif data["message"] == "Stock already exists":

            st.sidebar.warning("⚠️ Company already exists")

        else:

            st.sidebar.success("✅ Stock Added Successfully")

            st.rerun()
if delete:

    if stock_input.strip() == "":
        st.sidebar.warning("Please enter a ticker.")

    else:

        response = requests.delete(
            f"{API_URL}/stocks/{stock_input.upper()}"
        )

        data = response.json()

        if data["message"] == "Stock deleted successfully":

            st.sidebar.success("🗑 Company Deleted")

            st.rerun()

        else:

            st.sidebar.error("❌ Company not found")
# Fetch all stocks
response = requests.get(f"{API_URL}/stocks")
stocks = response.json()

df = pd.DataFrame(stocks)

# Sidebar
company = st.sidebar.selectbox(
    "Select Company",
    df["ticker"]
)

# Fetch selected stock
stock = requests.get(f"{API_URL}/stocks/{company}").json()

# Metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("Price", f"₹{stock['price']}")
col2.metric("Market Cap", f"{stock['market_cap']:,}")
col3.metric("P/E Ratio", stock["pe_ratio"])
col4.metric("EPS", stock["eps"])

st.divider()

# Historical Data
history = requests.get(f"{API_URL}/history/{company}").json()

history_df = pd.DataFrame(history)
chart_type = st.radio(
    "Chart Type",
    ["Line Chart", "Candlestick"]
)
if chart_type == "Line Chart":

    fig = px.line(
        history_df,
        x="date",
        y="close",
        title=f"{company} Price"
    )

else:

    fig = go.Figure(data=[go.Candlestick(
        x=history_df["date"],
        open=history_df["open"],
        high=history_df["high"],
        low=history_df["low"],
        close=history_df["close"]
    )])

    fig.update_layout(
        title=f"{company} Candlestick Chart"
    )

st.plotly_chart(fig, use_container_width=True)
fig = px.line(
    history_df,
    x="date",
    y="close",
    title=f"{company} - Last 6 Months"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("Company Comparison")

selected = st.multiselect(
    "Compare Companies",
    df["ticker"],
    default=df["ticker"][:3]
)

compare = df[df["ticker"].isin(selected)]

fig = px.bar(
    compare,
    x="ticker",
    y="price",
    color="ticker",
    title="Current Price Comparison"
)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(compare)
st.subheader("🤖 AI Overview")

st.info(ai_summary(stock))
last = history_df.iloc[-1]

if last["close"] > last["open"]:
    st.success("🟢 Bullish today")

else:
    st.error("🔴 Bearish today")
history_df["MA20"] = history_df["close"].rolling(20).mean()

fig = px.line(
    history_df,
    x="date",
    y=["close", "MA20"],
    title="Price with 20-Day Moving Average"
)

st.plotly_chart(fig)
st.download_button(
    "Download Data",
    df.to_csv(index=False),
    "stocks.csv",
    "text/csv"
)
# ==========================
# PORTFOLIO ANALYSIS
# ==========================

st.divider()
st.header("📁 Portfolio Analysis")

portfolio_stocks = st.multiselect(
    "Select Stocks for Your Portfolio",
    df["ticker"].tolist()
)

portfolio = []

for ticker in portfolio_stocks:

    quantity = st.number_input(
        f"Quantity of {ticker}",
        min_value=1,
        value=1,
        key=f"qty_{ticker}"
    )

    buy_price = st.number_input(
        f"Buy Price of {ticker} (₹)",
        min_value=0.0,
        value=float(
            df[df["ticker"] == ticker]["price"].values[0]
        ),
        key=f"buy_{ticker}"
    )

    current_price = float(
        df[df["ticker"] == ticker]["price"].values[0]
    )

    investment = buy_price * quantity
    current_value = current_price * quantity
    profit = current_value - investment

    portfolio.append({
        "Ticker": ticker,
        "Quantity": quantity,
        "Buy Price": buy_price,
        "Current Price": current_price,
        "Investment": investment,
        "Current Value": current_value,
        "Profit/Loss": profit
    })

if portfolio:

    portfolio_df = pd.DataFrame(portfolio)

    total_investment = portfolio_df["Investment"].sum()
    total_value = portfolio_df["Current Value"].sum()
    total_profit = portfolio_df["Profit/Loss"].sum()

    roi = (total_profit / total_investment) * 100

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Investment",
        f"₹{total_investment:,.2f}"
    )

    c2.metric(
        "Current Value",
        f"₹{total_value:,.2f}"
    )

    c3.metric(
        "Profit/Loss",
        f"₹{total_profit:,.2f}"
    )

    c4.metric(
        "ROI",
        f"{roi:.2f}%"
    )

    st.subheader("Portfolio Holdings")

    st.dataframe(portfolio_df)

    # Portfolio Allocation
    st.subheader("Portfolio Allocation")

    fig = px.pie(
        portfolio_df,
        names="Ticker",
        values="Current Value",
        title="Portfolio Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

    # AI Overview
    st.subheader("🤖 AI Portfolio Insights")

    largest = portfolio_df.loc[
        portfolio_df["Current Value"].idxmax()
    ]

    if roi > 10:
        st.success("✅ Your portfolio is performing well with a healthy return.")

    elif roi >= 0:
        st.info("📈 Your portfolio is in profit but has room for improvement.")

    else:
        st.error("📉 Your portfolio is currently in a loss.")

    st.write(
        f"🏆 Largest holding: **{largest['Ticker']}**"
    )

    st.write(
        f"💰 Current Portfolio Value: **₹{total_value:,.2f}**"
    )

    if len(portfolio_df) < 3:
        st.warning(
            "⚠️ Consider diversifying your portfolio by adding more stocks."
        )

    else:
        st.success(
            "✅ Your portfolio appears reasonably diversified."
        )
st.info(
    "💡 Enter the quantity and purchase price for each stock to analyze your portfolio performance."
)

