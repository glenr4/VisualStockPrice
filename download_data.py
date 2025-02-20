import yfinance as yf
import os
import var

# Variables
stockSymbol = var.stockSymbol
startDate = var.startDate
endDate = var.endDate
interval = var.interval

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
