# app.py
# This backend is now updated with the condensed snapshot of instruments.

from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf
import pandas as pd
from datetime import date, timedelta

# Initialize the Flask app
app = Flask(__name__)
# Enable CORS to prevent browser errors
CORS(app)


# --- Data Fetching and Calculation Logic ---

def calculate_atrp(hist):
    """Calculates the 14-day Average True Range Percentage (ATRP)."""
    high_low = hist['High'] - hist['Low']
    high_close = (hist['High'] - hist['Close'].shift(1)).abs()
    low_close = (hist['Low'] - hist['Close'].shift(1)).abs()
    
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    
    atr_14d = true_range.rolling(window=14).mean().iloc[-1]
    
    atrp = (atr_14d / hist['Close'].iloc[-1]) * 100
    return atrp

def get_instrument_data(ticker):
    """Fetches and calculates all metrics for a single instrument."""
    try:
        instrument = yf.Ticker(ticker)
        hist = instrument.history(period="1y")

        if hist.empty:
            raise ValueError("No historical data found.")

        # --- Calculations ---
        current_price = hist['Close'].iloc[-1]
        daily_pct_change = hist['Close'].pct_change().iloc[-1] * 100
        atrp_14d = calculate_atrp(hist)
        
        short_ma = hist['Close'].rolling(window=20).mean().iloc[-1]
        long_ma = hist['Close'].rolling(window=50).mean().iloc[-1]
        monthly_trend = "Uptrend" if short_ma > long_ma else "Downtrend"
        
        monthly_pct_change = hist['Close'].pct_change(periods=21).iloc[-1] * 100
        
        current_year = date.today().year
        start_of_year_price = hist[hist.index.year == current_year]['Open'].iloc[0]
        ytd_pct_change = ((hist['Close'].iloc[-1] - start_of_year_price) / start_of_year_price) * 100

        # Return data in a dictionary
        return {
            "instrument": ticker,
            "current_price": current_price,
            "daily_pct_change": daily_pct_change,
            "atrp": atrp_14d,
            "monthly_trend": monthly_trend,
            "monthly_pct_change": monthly_pct_change,
            "ytd_pct_change": ytd_pct_change,
        }
    except Exception as e:
        print(f"Error fetching instrument data for {ticker}: {e}")
        return {
            "instrument": f"{ticker} (Error)", "current_price": 0, "daily_pct_change": 0, "atrp": 0, "monthly_trend": "N/A",
            "monthly_pct_change": 0, "ytd_pct_change": 0,
        }

# --- API Endpoint ---

@app.route('/api/instruments')
def serve_instrument_data():
    instrument_groups = {
        "Treasury Yields": ["^TNX", "^TYX"],
        "US Equity Indices": ["ES=F", "NQ=F", "RTY=F", "^VIX"],
        "Energy": ["CL=F", "BZ=F", "NG=F", "TTF=F"],
        "Metals": ["GC=F", "SI=F"],
        "Currencies": ["DX-Y.NYB", "EURUSD=X", "JPY=X", "GBPUSD=X"]
    }
    
    all_data = []
    for group_name, tickers in instrument_groups.items():
        all_data.append({"is_header": True, "group_name": group_name})
        for ticker in tickers:
            data = get_instrument_data(ticker)
            data["is_header"] = False
            all_data.append(data)
            
    return jsonify(all_data)


# --- Run the Server ---
if __name__ == '__main__':
    app.run(debug=True)
