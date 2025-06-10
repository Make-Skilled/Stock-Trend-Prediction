import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_stock_data(symbol, start_date, end_date, initial_price, volatility=0.02):
    """Generate sample stock data for a given symbol and date range."""
    # Generate date range
    date_range = pd.date_range(start=start_date, end=end_date, freq='B')  # 'B' for business days
    
    # Initialize price series
    prices = [initial_price]
    
    # Generate random walk with drift
    for _ in range(len(date_range) - 1):
        # Random price change
        change = np.random.normal(0, volatility)
        new_price = prices[-1] * (1 + change)
        prices.append(new_price)
    
    # Create DataFrame
    df = pd.DataFrame({
        'date': date_range,
        'open': prices,
        'close': prices,
        'high': [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
        'low': [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
        'volume': [int(np.random.normal(1000000, 500000)) for _ in range(len(prices))],
        'Name': symbol
    })
    
    # Ensure high is highest and low is lowest
    df['high'] = df[['open', 'close', 'high']].max(axis=1)
    df['low'] = df[['open', 'close', 'low']].min(axis=1)
    
    return df

def main():
    # Generate data for multiple stocks
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META']
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2023, 12, 31)
    initial_prices = [150, 2800, 200, 3300, 250]  # Different starting prices for each stock
    
    # Generate data for each stock
    all_data = []
    for symbol, initial_price in zip(symbols, initial_prices):
        stock_data = generate_stock_data(symbol, start_date, end_date, initial_price)
        all_data.append(stock_data)
    
    # Combine all data
    combined_data = pd.concat(all_data, ignore_index=True)
    
    # Save to CSV
    output_path = 'all_stocks.csv'
    combined_data.to_csv(output_path, index=False)
    print(f"Generated sample stock data saved to {output_path}")
    print("\nSample of the generated data:")
    print(combined_data.head())
    print("\nData shape:", combined_data.shape)
    print("\nAvailable symbols:", combined_data['Name'].unique())

if __name__ == "__main__":
    main() 