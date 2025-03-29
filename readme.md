# Visual Stock Price Direction Predictor

## Setup

1. Install Python v3.13 or higher
1. Install Anaconda
1. Restore packages and create a new environment:

```sh
conda env create -n VisualStockPrice --file environment.yml
```

## Run It

### Input Parameters

Set in the `var.py` file.

### From a CLI:

If price data has been downloaded from investing.com, then update variables in `var.py`:
* `stockSymbol`
* `interval`

Then run:
```sh
python convert_investing.com_data.py
```
If downloading data, then update variables in `var.py`:
* `stockSymbol`
* `interval`
* `startDate`
* `endDate`

Then run:
```sh
python download_data.py
```

Update the price movement parameters in `var.py`:
* `large_move_max_candles`
* `large_move_threshold_percent`
* `pre_large_move_candles`

Then run:
```sh
python generate_candles.py
python balance_images.py
python split_images.py
python train_model.py
python predict_price_move.py
```

# To do

- Create classes instead of stand alone files
