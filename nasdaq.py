import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# get nasdaq 100
def get_nasdaq_tickers() -> list:
    '''
    get all 100 nasdaq tickers from wiki,
    return a list of tickers (AAPL, MSFT, etc.)
    '''
    nasdaq_url = "https://en.wikipedia.org/wiki/NASDAQ-100"
    nasdaq_tables = pd.read_html(nasdaq_url)     
    tickers = nasdaq_tables[4]['Ticker'].tolist()
    return tickers

# get data from past 5 years
def get_stock_data(tickers: list) -> dict:
    '''
    input a list of tickers (AAPL, MSFT, etc.)
    return a dictionary of dataframes with stock data
    '''
    end_date = datetime.today()
    
    # get data from past 5 years
    start_date = end_date - timedelta(days=5*365)
    
    stock_data = {}
    for ticker in tickers:
        print(f"Downloading 5-minute interval data for {ticker}...")
        stock = yf.Ticker(ticker)
        stock_df = stock.history(interval="5m", start=start_date, end=end_date)
        stock_data[ticker] = stock_df
    
    return stock_data

if __name__ == "__main__":
    # get tickers
    tickers = get_nasdaq_tickers()

    # get data
    nasdaq_stock_data = get_stock_data(tickers)

    # save csv
    for ticker, data in nasdaq_stock_data.items():
        data.to_csv(f'./raw_data/nasdaq/{ticker}_data.csv')
        print(f"Data for {ticker} saved to {ticker}_data.csv")
