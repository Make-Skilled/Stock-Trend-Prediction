import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ta.trend import SMAIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.volatility import BollingerBands
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings('ignore')

class StockAnalyzer:
    def __init__(self, csv_path):
        """Initialize the StockAnalyzer with the path to the CSV file."""
        try:
            self.df = pd.read_csv(csv_path)
            print("Successfully loaded CSV file")
            print("Available columns:", self.df.columns.tolist())
            self.process_data()
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find the CSV file at {csv_path}. Please make sure the file exists and the path is correct.")
        except Exception as e:
            raise Exception(f"Error loading CSV file: {str(e)}")
        
    def process_data(self):
        """Process and clean the stock data."""
        # Map common column names
        column_mapping = {
            'date': 'Date',
            'timestamp': 'Date',
            'datetime': 'Date',
            'symbol': 'Name',
            'ticker': 'Name',
            'name': 'Name',
            'Name': 'Name',
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close',
            'volume': 'Volume'
        }
        
        # Rename columns if they exist with different names
        for old_col, new_col in column_mapping.items():
            if old_col in self.df.columns and new_col not in self.df.columns:
                self.df.rename(columns={old_col: new_col}, inplace=True)
        
        # Check for required columns
        required_columns = ['Date', 'Name', 'Open', 'High', 'Low', 'Close', 'Volume']
        missing_columns = [col for col in required_columns if col not in self.df.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}. Please ensure your CSV file has these columns.")
        
        # Convert date column to datetime
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        
        # Sort by date
        self.df = self.df.sort_values('Date')
        
        # Calculate technical indicators
        self.calculate_technical_indicators()
        
    def calculate_technical_indicators(self):
        """Calculate technical indicators for analysis."""
        # Simple Moving Averages
        self.df['SMA_20'] = SMAIndicator(close=self.df['Close'], window=20).sma_indicator()
        self.df['SMA_50'] = SMAIndicator(close=self.df['Close'], window=50).sma_indicator()
        self.df['SMA_200'] = SMAIndicator(close=self.df['Close'], window=200).sma_indicator()
        
        # Exponential Moving Averages
        self.df['EMA_20'] = EMAIndicator(close=self.df['Close'], window=20).ema_indicator()
        self.df['EMA_50'] = EMAIndicator(close=self.df['Close'], window=50).ema_indicator()
        
        # MACD
        macd = MACD(close=self.df['Close'])
        self.df['MACD'] = macd.macd()
        self.df['MACD_Signal'] = macd.macd_signal()
        self.df['MACD_Hist'] = macd.macd_diff()
        
        # RSI
        self.df['RSI'] = RSIIndicator(close=self.df['Close']).rsi()
        
        # Bollinger Bands
        bollinger = BollingerBands(close=self.df['Close'])
        self.df['BB_Upper'] = bollinger.bollinger_hband()
        self.df['BB_Lower'] = bollinger.bollinger_lband()
        self.df['BB_Middle'] = bollinger.bollinger_mavg()
        
        # Stochastic Oscillator
        stoch = StochasticOscillator(high=self.df['High'], low=self.df['Low'], close=self.df['Close'])
        self.df['Stoch_K'] = stoch.stoch()
        self.df['Stoch_D'] = stoch.stoch_signal()
        
    def identify_patterns(self, symbol, window=20):
        """Identify price patterns in the stock data."""
        stock_data = self.df[self.df['Name'] == symbol].copy()
        
        if stock_data.empty:
            raise ValueError(f"No data found for symbol: {symbol}")
        
        patterns = []
        
        # Calculate price changes and indicators
        stock_data['Price_Change'] = stock_data['Close'].pct_change()
        stock_data['Volume_Change'] = stock_data['Volume'].pct_change()
        
        # Identify patterns
        for i in range(window, len(stock_data)):
            window_data = stock_data.iloc[i-window:i]
            current_price = stock_data.iloc[i]['Close']
            
            # Trend Patterns
            if all(window_data['Close'].diff().dropna() > 0):
                patterns.append({
                    'date': stock_data.iloc[i]['Date'],
                    'pattern': 'Strong Uptrend',
                    'confidence': 'High',
                    'description': 'Consistent upward price movement'
                })
            elif all(window_data['Close'].diff().dropna() < 0):
                patterns.append({
                    'date': stock_data.iloc[i]['Date'],
                    'pattern': 'Strong Downtrend',
                    'confidence': 'High',
                    'description': 'Consistent downward price movement'
                })
            
            # Consolidation Pattern
            elif window_data['Close'].std() < window_data['Close'].mean() * 0.02:
                patterns.append({
                    'date': stock_data.iloc[i]['Date'],
                    'pattern': 'Consolidation',
                    'confidence': 'Medium',
                    'description': 'Price moving sideways in a tight range'
                })
            
            # Golden Cross (SMA 50 crosses above SMA 200)
            if (window_data['SMA_50'].iloc[-2] <= window_data['SMA_200'].iloc[-2] and 
                window_data['SMA_50'].iloc[-1] > window_data['SMA_200'].iloc[-1]):
                patterns.append({
                    'date': stock_data.iloc[i]['Date'],
                    'pattern': 'Golden Cross',
                    'confidence': 'High',
                    'description': '50-day SMA crosses above 200-day SMA'
                })
            
            # Death Cross (SMA 50 crosses below SMA 200)
            if (window_data['SMA_50'].iloc[-2] >= window_data['SMA_200'].iloc[-2] and 
                window_data['SMA_50'].iloc[-1] < window_data['SMA_200'].iloc[-1]):
                patterns.append({
                    'date': stock_data.iloc[i]['Date'],
                    'pattern': 'Death Cross',
                    'confidence': 'High',
                    'description': '50-day SMA crosses below 200-day SMA'
                })
            
            # RSI Patterns
            if window_data['RSI'].iloc[-1] > 70:
                patterns.append({
                    'date': stock_data.iloc[i]['Date'],
                    'pattern': 'Overbought',
                    'confidence': 'Medium',
                    'description': 'RSI above 70 indicates potential overbought condition'
                })
            elif window_data['RSI'].iloc[-1] < 30:
                patterns.append({
                    'date': stock_data.iloc[i]['Date'],
                    'pattern': 'Oversold',
                    'confidence': 'Medium',
                    'description': 'RSI below 30 indicates potential oversold condition'
                })
            
            # Bollinger Band Patterns
            if current_price > window_data['BB_Upper'].iloc[-1]:
                patterns.append({
                    'date': stock_data.iloc[i]['Date'],
                    'pattern': 'Above Upper Band',
                    'confidence': 'Medium',
                    'description': 'Price above upper Bollinger Band'
                })
            elif current_price < window_data['BB_Lower'].iloc[-1]:
                patterns.append({
                    'date': stock_data.iloc[i]['Date'],
                    'pattern': 'Below Lower Band',
                    'confidence': 'Medium',
                    'description': 'Price below lower Bollinger Band'
                })
        
        return pd.DataFrame(patterns)

    def plot_stock_trend(self, symbol, start_date=None, end_date=None):
        """Create an interactive plot of stock price and indicators."""
        stock_data = self.df[self.df['Name'] == symbol].copy()
        
        if stock_data.empty:
            raise ValueError(f"No data found for symbol: {symbol}")
        
        if start_date:
            stock_data = stock_data[stock_data['Date'] >= start_date]
        if end_date:
            stock_data = stock_data[stock_data['Date'] <= end_date]
            
        # Create figure with secondary y-axis
        fig = make_subplots(rows=3, cols=1, 
                           shared_xaxes=True,
                           vertical_spacing=0.05,
                           row_heights=[0.6, 0.2, 0.2])

        # Add candlestick chart
        fig.add_trace(go.Candlestick(x=stock_data['Date'],
                                    open=stock_data['Open'],
                                    high=stock_data['High'],
                                    low=stock_data['Low'],
                                    close=stock_data['Close'],
                                    name='OHLC'),
                     row=1, col=1)

        # Add moving averages
        fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['SMA_20'],
                                name='SMA 20',
                                line=dict(color='orange')),
                     row=1, col=1)
        
        fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['SMA_50'],
                                name='SMA 50',
                                line=dict(color='blue')),
                     row=1, col=1)
        
        fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['SMA_200'],
                                name='SMA 200',
                                line=dict(color='purple')),
                     row=1, col=1)

        # Add Bollinger Bands
        fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['BB_Upper'],
                                name='BB Upper',
                                line=dict(color='gray', dash='dash')),
                     row=1, col=1)
        
        fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['BB_Lower'],
                                name='BB Lower',
                                line=dict(color='gray', dash='dash')),
                     row=1, col=1)

        # Add RSI
        fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['RSI'],
                                name='RSI',
                                line=dict(color='purple')),
                     row=2, col=1)

        # Add RSI levels
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

        # Add MACD
        fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['MACD'],
                                name='MACD',
                                line=dict(color='blue')),
                     row=3, col=1)
        
        fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['MACD_Signal'],
                                name='MACD Signal',
                                line=dict(color='orange')),
                     row=3, col=1)
        
        fig.add_trace(go.Bar(x=stock_data['Date'], y=stock_data['MACD_Hist'],
                            name='MACD Histogram',
                            marker_color='gray'),
                     row=3, col=1)

        # Update layout
        fig.update_layout(
            title=f'{symbol} Stock Analysis',
            yaxis_title='Price',
            yaxis2_title='RSI',
            yaxis3_title='MACD',
            xaxis_rangeslider_visible=False,
            height=1000
        )

        return fig

    def get_stock_summary(self, symbol):
        """Generate a summary of key statistics for a given stock."""
        stock_data = self.df[self.df['Name'] == symbol].copy()
        
        if stock_data.empty:
            raise ValueError(f"No data found for symbol: {symbol}")
        
        # Calculate additional metrics
        daily_returns = stock_data['Close'].pct_change()
        annualized_return = daily_returns.mean() * 252
        annualized_volatility = daily_returns.std() * np.sqrt(252)
        sharpe_ratio = annualized_return / annualized_volatility if annualized_volatility != 0 else 0
        
        summary = {
            'Symbol': symbol,
            'Current Price': f"${stock_data['Close'].iloc[-1]:.2f}",
            '52-Week High': f"${stock_data['High'].max():.2f}",
            '52-Week Low': f"${stock_data['Low'].min():.2f}",
            'Average Volume': f"{stock_data['Volume'].mean():,.0f}",
            'Volatility': f"{annualized_volatility:.2%}",
            'Annual Return': f"{annualized_return:.2%}",
            'Sharpe Ratio': f"{sharpe_ratio:.2f}",
            'RSI': f"{stock_data['RSI'].iloc[-1]:.2f}",
            'MACD': f"{stock_data['MACD'].iloc[-1]:.2f}",
            'SMA_20': f"${stock_data['SMA_20'].iloc[-1]:.2f}",
            'SMA_50': f"${stock_data['SMA_50'].iloc[-1]:.2f}",
            'SMA_200': f"${stock_data['SMA_200'].iloc[-1]:.2f}"
        }
        
        return pd.Series(summary) 