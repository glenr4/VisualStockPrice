import pandas as pd

source_file = "./data/GC=F_2024-01-01_2024-12-31.csv"

# Load the stock data from the saved CSV file
stock_data = pd.read_csv(source_file, index_col=0, parse_dates=True)

# Print the loaded data
print(stock_data.head())