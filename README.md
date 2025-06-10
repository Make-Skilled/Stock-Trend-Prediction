# Stock Trend Prediction System

This project provides tools for analyzing historical stock data, visualizing trends, and identifying patterns. It focuses on visualization and pattern recognition rather than actual trading recommendations.

## Features

- Interactive stock price visualization with candlestick charts
- Technical indicators calculation (SMA, EMA, RSI)
- Pattern recognition for identifying trends and consolidation periods
- Stock summary statistics
- Interactive HTML reports

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Make sure your stock data is in the `all_stocks.csv` file with the following columns:
   - Date
   - Symbol
   - Open
   - High
   - Low
   - Close
   - Volume

2. Run the analysis script:
```bash
python src/analyze_stocks.py
```

This will:
- Analyze the first 5 stocks in the dataset
- Generate interactive HTML visualizations in the `output` directory
- Print summary statistics and identified patterns

## Custom Analysis

To analyze specific stocks or customize the analysis, you can modify the `analyze_stocks.py` script or use the `StockAnalyzer` class directly:

```python
from stock_analyzer import StockAnalyzer

# Initialize analyzer
analyzer = StockAnalyzer('path_to_your_csv')

# Get stock summary
summary = analyzer.get_stock_summary('AAPL')

# Generate interactive plot
fig = analyzer.plot_stock_trend('AAPL')

# Identify patterns
patterns = analyzer.identify_patterns('AAPL')
```

## Output

The system generates:
1. Interactive HTML visualizations with:
   - Candlestick charts
   - Moving averages (20-day and 50-day SMA)
   - RSI indicator
2. Pattern recognition results
3. Summary statistics including:
   - Current price
   - 52-week high/low
   - Average volume
   - Volatility
   - Technical indicators

## Note

This system is for educational and research purposes only. The analysis and patterns identified should not be used as financial advice or for actual trading decisions.