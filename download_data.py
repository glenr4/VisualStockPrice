import yfinance as yf
import os

# Variables
stockSymbol = "^AORD" # Australian All Ordinaries Index
startDate = '2015-01-01'
endDate = '2024-12-31'
interval = '1d'

# Create sub-folders
if not os.path.exists("data"):
    os.mkdir("data")

# Download price data 
stock_data = yf.download(stockSymbol, 
                         start=startDate, 
                         end=endDate, 
                         interval=interval, 
                         multi_level_index=False)

# Save the data to a CSV file
stock_data.to_csv('./data/{}_{}_{}_{}.csv'.format(stockSymbol, startDate, endDate, interval))
