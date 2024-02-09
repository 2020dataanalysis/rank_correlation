import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# Function to get historical stock price data
def get_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data['Adj Close']

# Function to calculate z-score
def calculate_zscore(series):
    return (series - series.mean()) / series.std()

# Define the stock tickers and date range
stock_ticker_1 = "AAPL"
stock_ticker_2 = "MSFT"
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

# Get historical stock price data for both stocks for the last 30 days
stock_prices_1 = get_stock_data(stock_ticker_1, start_date, end_date)
stock_prices_2 = get_stock_data(stock_ticker_2, start_date, end_date)

# Check if there is sufficient data for trading
if stock_prices_1.empty or stock_prices_2.empty:
    print("Insufficient data for trading.")
else:
    # Calculate the spread between the two stocks
    spread = stock_prices_1 - stock_prices_2

    # Calculate the z-score of the spread
    zscore = calculate_zscore(spread)

    # Define trading signals based on z-score
    entry_threshold = 1.0
    exit_threshold = 0.0

    # Initialize position and logs
    position = 0
    buy_log = []
    sell_log = []
    profit_log = []

    # Iterate over each day and check for trading signals
    for i in range(len(zscore)):
        if zscore[i] > entry_threshold and position == 0:  # Buy stock 1
            print(f"Buy {stock_ticker_1}")
            buy_log.append((stock_ticker_1, stock_prices_1.index[i], stock_prices_1[i]))
            position = 1
            entry_time = stock_prices_1.index[i]
        elif zscore[i] < exit_threshold and position != 0:  # Sell stock 1
            print(f"Sell {stock_ticker_1}")
            sell_log.append((stock_ticker_1, stock_prices_1.index[i], stock_prices_1[i]))
            position = 0

            # Calculate profit when closing the position
            if buy_log:
                entry_price = buy_log[-1][2]
                exit_price = stock_prices_1[i]
                profit = (exit_price - entry_price) * 1  # Assuming position size is 1
                profit_log.append(profit)

        # Exit position after 1 minute
        if position == 1 and stock_prices_1.index[i] - entry_time >= timedelta(minutes=1):
            print(f"Sell {stock_ticker_1} after 1 minute")
            sell_log.append((stock_ticker_1, stock_prices_1.index[i], stock_prices_1[i]))
            position = 0

            # Calculate profit when closing the position after 1 minute
            if buy_log:
                entry_price = buy_log[-1][2]
                exit_price = stock_prices_1[i]
                profit = (exit_price - entry_price) * 1  # Assuming position size is 1
                profit_log.append(profit)
                entry_time = None

    # Calculate total profit
    total_profit = sum(profit_log)
    print("Total Profit:", total_profit)
