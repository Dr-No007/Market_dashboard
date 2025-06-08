# Market dahsboard project
# First Objectives
# 1. Importing necessary libraries 
# 2 Define the list of futures symbols to track
# 3. fetch historical data for each symbol
# 4. IDisplay data for 1 insrument

#step 1 importing necessary libraries
# Using 'yfinance' to fetch historical data
import yfinance as yf

# using 'pandass' for data manipulation(yfinance returns data in a pandas DataFrame)
import pandas as pd

#set a pandas option to display all columns in dataframe(helpful for adding more later)
pd.set_option('display.max_columns', None)

#step 2 define instruments
futures_tickers = ["ES=F", "NQ=F", "CL=F", "GC=F"]

#step 3 fetch historical data for each symbol
#create a dictionary to hold the data this will be used for storing data as a key
historical_data = {}
print("fetching data...")

#create a loop to fetch data for each ticker
for ticker in futures_tickers:
    try:
        futures = yf.Ticker(ticker) # create a ticker for current future
        data = futures.history(period="2y") # fetch historical data for the last 2 years
        data = data[['Open', 'High', 'Low', 'Close', 'Volume']]  # select only the relevant columns
        historical_data[ticker] = data # store the data in the dictionary
        print(f"successfully fetched data for {ticker}")
    except Exception as e: 
        print(f"Could not fetch data for {ticker}. Error: {e}") # if there is an error, print it
print("\nData fetching complete.")

#step 4 display data for one instrument
if "ES=F" in historical_data:
    print("\n--- sample data for ES=F ---")
print(historical_data["ES=F"].tail(1))  # display the last 5 rows of data for ES=F