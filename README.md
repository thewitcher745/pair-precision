# Pair Precisions

Utilities to compute price precision (maximum decimal places) for USDT pairs across multiple exchanges using their public market/kline endpoints.

## Project Structure
- `precision_binance.py`
- `precision_bybit.py`
- `precision_okx.py`
- `precision_bitget.py`
- `precision_bingx.py`
- `precision_mexc.py`
- `precision_lbank.py`
- `logo_list.json` (input; see note below)
- `precisions_*.csv` (outputs per exchange)

## Requirements
- Python 3.9+
- `requests`

Install dependencies:
```bash
pip install requests
```

## Input: coin list
All scripts load coin tickers from `logo_list.json`.

## How it works
For each symbol, each script:
- fetches a small set of recent candlesticks from the exchange API
- collects open/high/low/close samples
- computes the maximum number of decimal places across samples
- writes `precisions_<exchange>.csv` with `symbol,precision` rows

## Usage
Run individual scripts as needed. Examples:
```bash
python precision_binance.py
python precision_bybit.py
python precision_okx.py
python precision_bitget.py
python precision_bingx.py
python precision_mexc.py
python precision_lbank.py
```
Outputs are written to the repository root as CSV files, e.g. `precisions_binance.csv`.

## Notes and troubleshooting
- Ensure symbols are quoted exactly as the exchange lists them against USDT (e.g., `BTC`, not `BTCUSDT`). The scripts append `USDT`/`-USDT` as required per API.
- If an API call fails or returns no data for a symbol, that symbol is skipped.
- Be mindful of exchange rate limits; running many scripts back-to-back on large symbol sets may hit limits.
- Network errors or schema differences can cause exceptions; scripts are written to skip problematic symbols and continue.