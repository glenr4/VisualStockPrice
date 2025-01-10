import yfinance as yf
import os

# Variables
stockSymbol = "GC=F"    # Gold futures
startDate = '2024-01-01'
endDate = '2024-12-31'

# Create sub-folders
if not os.path.exists("data"):
    os.mkdir("data")

# Download price data 
stock_data = yf.download(stockSymbol, start='2024-01-01', end='2024-12-31')

# Save the data to a CSV file
stock_data.to_csv('./data/{}_{}_{}.csv'.format(stockSymbol, startDate, endDate))
