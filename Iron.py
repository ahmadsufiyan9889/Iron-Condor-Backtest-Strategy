import pandas as pd
import numpy as np
import random

# Simulated options data for illustration
def simulate_options_data():
    dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq='B')  # Business days
    data = []
    for date in dates:
        # Simulate option prices and deltas
        market_price = random.uniform(15000, 16000)
        call_price = market_price + 600
        put_price = market_price - 400
        call_delta = 0.08
        put_delta = 0.08
        data.append([date, market_price, call_price, put_price, call_delta, put_delta])
    df = pd.DataFrame(data, columns=["Date", "MarketPrice", "CallPrice", "PutPrice", "CallDelta", "PutDelta"])
    return df

# Function to calculate strikes with delta
def calculate_strikes(data, delta):
    call_strike = data['MarketPrice'] + 600
    put_strike = data['MarketPrice'] - 400
    return call_strike, put_strike

# Iron Condor strategy implementation
def iron_condor_strategy(data, initial_capital, profit_target, loss_limit):
    results = []
    capital = initial_capital
    for index, row in data.iterrows():
        # Entry criteria
        entry_call_sell = row['CallPrice']
        entry_put_sell = row['PutPrice']
        buy_call_price = entry_call_sell * 1.06
        buy_put_price = entry_put_sell * 0.94
        
        max_profit = (entry_call_sell + entry_put_sell) - (buy_call_price + buy_put_price)
        stop_loss = max_profit * loss_limit
        profit_threshold = max_profit * profit_target

        # Simulate PnL
        pnl = random.uniform(-stop_loss, profit_threshold)
        capital += pnl
        results.append({"Date": row["Date"], "PnL": pnl, "Capital": capital})
        
        # Stop if capital drops significantly
        if pnl <= -stop_loss:
            break
    return results

# Backtest Iron Condor
def backtest_iron_condor(ticker, delta, initial_capital, profit_target, loss_limit):
    # Simulated data
    data = simulate_options_data()

    # Calculate strikes for Iron Condor
    call_strike, put_strike = calculate_strikes(data, delta)

    # Run the Iron Condor strategy
    results = iron_condor_strategy(data, initial_capital, profit_target, loss_limit)
    return pd.DataFrame(results)

# Parameters
tickers = ["NIFTY", "BANKNIFTY", "MIDCAPNIFTY", "FINNIFTY", "SENSEX"]
delta = 0.08
initial_capital = 1000000  # 10 lakhs
profit_target = 0.4  # 40% of max profit
loss_limit = 0.25  # 25% of max profit

# Run the backtest for each ticker
for ticker in tickers:
    print(f"Results for {ticker}:")
    results = backtest_iron_condor(ticker, delta, initial_capital, profit_target, loss_limit)
    print(results.head())  # Display the first few results for illustration
