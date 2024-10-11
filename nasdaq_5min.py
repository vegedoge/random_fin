import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# 获取纳斯达克100的成分股
def get_nasdaq_tickers():
    nasdaq_url = "https://en.wikipedia.org/wiki/NASDAQ-100"
    nasdaq_tables = pd.read_html(nasdaq_url)
    
    # 确保选择正确的表和列
    tickers = nasdaq_tables[4]['Ticker'].tolist()
    return tickers

# 分段获取5分钟间隔的股票数据
def get_stock_data_for_period(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    try:
        stock_df = stock.history(interval="5m", start=start_date, end=end_date)
        return stock_df
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()

# 获取过去五年的股票数据，每30天为一个周期
def get_stock_data(ticker, years=5):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=years*365)

    all_data = pd.DataFrame()

    # 每次抓取30天的数据，直到覆盖整个时间段
    while end_date > start_date:
        period_start = end_date - timedelta(days=30)
        print(f"Downloading data for {ticker} from {period_start} to {end_date}...")
        
        # 获取当前时间段的数据
        stock_df = get_stock_data_for_period(ticker, period_start.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        
        # 将新数据拼接到总数据中
        if not stock_df.empty:
            all_data = pd.concat([stock_df, all_data])
        
        # 更新结束日期，继续获取之前的30天数据
        end_date = period_start
    
    return all_data

if __name__ == "__main__":
    # 获取纳斯达克100的股票代码
    tickers = get_nasdaq_tickers()

    # 获取单只股票的过去五年数据
    for ticker in tickers:
        stock_data = get_stock_data(ticker)

        # 保存数据到CSV文件
        if not stock_data.empty:
            stock_data.to_csv(f'{ticker}_5min_data.csv')
            print(f"Data for {ticker} saved to {ticker}_5min_data.csv")
        else:
            print(f"No data available for {ticker}")
