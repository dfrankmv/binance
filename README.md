# binance

A lightweight Python implementation of Binance's basic REST API.
It includes separate modules for different market types:

- `client.py` – Core HTTP client for interacting with the API.
- `spot.py` – Spot market operations.
- `futures.py` – Futures market operations.
- (Planned) `margin.py` – Margin trading operations.

With these modules, you can easily:

- Retrieve the latest price of a trading pair.
- Place, modify, and cancel orders.
- Access basic market and account data.

The goal is to keep the implementation simple, clear, and easy to extend for custom trading strategies.

## Installation
```
pip install git+https://github.com/dfrankmv/binance.git
```

## Usage
```python
from binance import *
```