import file_handling as fh

# Input variables used across the codebase
# Input data file expected to be in the format: ./data/{stockSymbol}_{startDate}_{endDate}_{interval}.csv
stockSymbol = "MGC"
startDate = '2025-01-01'
endDate = '2025-02-19'
interval = '30m'

# Price movement
large_move_max_candles=5
large_move_threshold_percent=4
pre_large_move_candles=50


# Yahoo finance symbols
"^AORD" # Australian All Ordinaries Index