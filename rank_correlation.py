#   Sammy Portillo
#   01.20.2024


import pandas as pd
import yfinance as yf
import warnings

# Suppress FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Function to get historical stock price data
def get_stock_data(ticker, start_date, end_date):
    # stock_data = yf.download(ticker, start=start_date, end=end_date)
    stock_data = yf.download(ticker, start=start_date, end=end_date, interval='1m')
    return stock_data['Adj Close']

# Function to calculate correlation matrix
def calculate_correlation_matrix(stock_prices):
    return stock_prices.corr()

# Define the list of stock tickers and date range
stock_tickers = [
    "MMM", "AXP", "AMGN", "AAPL", "BA", "CAT", "CVX", "CSCO", "KO", "DOW",
    "GS", "HD", "HON", "IBM", "INTC", "JNJ", "JPM", "MCD", "MRK", "MSFT",
    "NKE", "PG", "CRM", "TRV", "UNH", "V-Z", "V", "WBA", "WMT", "DIS"
]

start_date = '2024-02-09'
# end_date = '2024-01-05'
end_date = pd.to_datetime(start_date) + pd.DateOffset(days=1)

# Get historical stock price data for all stocks
stock_prices = pd.DataFrame()

for ticker in stock_tickers:
    stock_prices[ticker] = get_stock_data(ticker, start_date, end_date)

# print(stock_prices)

# Calculate correlation matrix
correlation_matrix = calculate_correlation_matrix(stock_prices)

# Display the correlation matrix
print("Correlation Matrix:")
print(correlation_matrix)

# Sort unique stock pairs by highest correlation
corr_pairs = correlation_matrix.unstack().sort_values(ascending=False)
unique_corr_pairs = corr_pairs[corr_pairs < 1].reset_index()
unique_corr_pairs.columns = ['Stock_1', 'Stock_2', 'Correlation']
unique_corr_pairs.drop_duplicates(subset=['Correlation'], inplace=True)
print("\nUnique Pairs with Highest Correlation:")
print(unique_corr_pairs.head(10))
