from flask import Flask, render_template, request, redirect, url_for, flash
import os
from stock_analyzer import StockAnalyzer
import plotly.io as pio

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

# Path to the CSV file
data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'all_stocks.csv')

# Initialize analyzer once
analyzer = StockAnalyzer(data_path)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Get unique stock names and sort them
    symbols = sorted(analyzer.df['Name'].unique())
    
    if request.method == 'POST':
        symbol = request.form.get('symbol')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        
        if not symbol:
            flash('Please select a stock symbol.')
            return redirect(url_for('index'))
            
        return redirect(url_for('results', symbol=symbol, start_date=start_date, end_date=end_date))
        
    return render_template('index.html', symbols=symbols)

@app.route('/results')
def results():
    symbol = request.args.get('symbol')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    try:
        summary = analyzer.get_stock_summary(symbol)
        patterns = analyzer.identify_patterns(symbol)
        fig = analyzer.plot_stock_trend(symbol, start_date, end_date)
        plot_html = pio.to_html(fig, full_html=False)
        patterns_table = patterns.tail(10).to_dict(orient='records') if not patterns.empty else []
        
        return render_template('results.html', 
                             symbol=symbol, 
                             summary=summary, 
                             patterns=patterns_table, 
                             plot_html=plot_html)
    except Exception as e:
        flash(str(e))
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 