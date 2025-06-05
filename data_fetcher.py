print("Hello, script is running!")
import yfinance as yf
print("Trying to fetch data...")
ticker = "ES=F"
try:
    data = yf.Ticker(ticker).history(period="1mo")
    print(f"Data for {ticker}:\n", data[['Open', 'High', 'Low', 'Close']].tail())
except Exception as e:
    print(f"Error: {e}")
print("Done!")