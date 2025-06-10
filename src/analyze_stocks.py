from stock_analyzer import StockAnalyzer
import plotly.io as pio
import os
import sys

def main():
    try:
        # Get the absolute path to the CSV file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(os.path.dirname(current_dir), 'all_stocks.csv')
        
        print(f"Looking for CSV file at: {csv_path}")
        
        # Initialize the analyzer with the CSV file
        analyzer = StockAnalyzer(csv_path)
        
        # Get unique stock symbols
        symbols = analyzer.df['Symbol'].unique()
        print(f"\nFound {len(symbols)} unique stocks in the dataset")
        print("Available symbols:", symbols[:5], "...")  # Show first 5 symbols
        
        # Example: Analyze a few stocks
        example_symbols = symbols[:5]  # Take first 5 stocks as examples
        
        # Create output directory if it doesn't exist
        output_dir = os.path.join(os.path.dirname(current_dir), 'output')
        os.makedirs(output_dir, exist_ok=True)
        
        for symbol in example_symbols:
            try:
                print(f"\nAnalyzing {symbol}:")
                
                # Get stock summary
                summary = analyzer.get_stock_summary(symbol)
                print("\nStock Summary:")
                print(summary)
                
                # Identify patterns
                patterns = analyzer.identify_patterns(symbol)
                if not patterns.empty:
                    print("\nIdentified Patterns:")
                    print(patterns.tail())
                
                # Create and save interactive plot
                fig = analyzer.plot_stock_trend(symbol)
                output_file = os.path.join(output_dir, f'{symbol}_analysis.html')
                pio.write_html(fig, output_file)
                print(f"\nSaved interactive plot to {output_file}")
                
            except Exception as e:
                print(f"Error analyzing {symbol}: {str(e)}")
                continue
                
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        print("\nPlease make sure the all_stocks.csv file exists in the project root directory.")
        print("The file should contain the following columns:")
        print("- Date (or date, timestamp, datetime)")
        print("- Symbol (or symbol, ticker)")
        print("- Open (or open)")
        print("- High (or high)")
        print("- Low (or low)")
        print("- Close (or close)")
        print("- Volume (or volume)")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 