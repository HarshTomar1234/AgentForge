import yfinance as yf
import matplotlib.pyplot as plt

def fetch_stock_data(symbol, start_date, end_date):
    stock = yf.Ticker(symbol)
    hist = stock.history(start=start_date, end=end_date)
    return hist

def plot_close_prices(data, symbol):
    data['Close'].plot(title=f'{symbol} Closing Price Trend', figsize=(10, 6))
    plt.xlabel('Date')
    plt.ylabel('Closing Price (USD)')
    plt.savefig(f'/content/coding/{symbol}_closing_price_trend.png')
    plt.show()

def plot_volumes(data, symbol):
    data['Volume'].plot(title=f'{symbol} Trading Volume', figsize=(10, 6), color='orange')
    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.savefig(f'/content/coding/{symbol}_trading_volume.png')
    plt.show()

def plot_moving_averages(data, symbol):
    moving_averages = [30, 50]
    for ma in moving_averages:
        data[f'MA_{ma}'] = data['Close'].rolling(window=ma).mean()
    data[['Close', 'MA_30', 'MA_50']].plot(title=f'{symbol} Moving Averages', figsize=(10, 6))
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.savefig(f'/content/coding/{symbol}_moving_averages.png')
    plt.show()

def plot_daily_returns(data, symbol):
    data['Daily Return'] = data['Close'].pct_change()
    data['Daily Return'].plot(title=f'{symbol} Daily Returns', figsize=(10, 6), color='red')
    plt.xlabel('Date')
    plt.ylabel('Daily Return')
    plt.savefig(f'/content/coding/{symbol}_daily_returns.png')
    plt.show()

def main():
    start_date = '2025-01-01'
    end_date = '2025-02-17'
    symbols = ['NVDA', 'TSLA']

    for symbol in symbols:
        data = fetch_stock_data(symbol, start_date, end_date)
        plot_close_prices(data, symbol)
        plot_volumes(data, symbol)
        plot_moving_averages(data, symbol)
        plot_daily_returns(data, symbol)

if __name__ == "__main__":
    main()
