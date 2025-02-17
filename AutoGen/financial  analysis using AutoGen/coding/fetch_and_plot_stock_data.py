import yfinance as yf
import matplotlib.pyplot as plt
from pandas import DataFrame
from datetime import datetime

def fetch_stock_data(symbol: str, start_date: str, end_date: str) -> DataFrame:
    stock = yf.Ticker(symbol)
    return stock.history(start=start_date, end=end_date)

def calculate_moving_average(data: DataFrame, period: int) -> DataFrame:
    return data['Close'].rolling(window=period).mean()

def plot_stock_data(stock_data: dict, title: str, file_name: str):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Plot YTD gain and moving averages on the first subplot
    for label, data in stock_data.items():
        ytd_gain = ((data['Close'] - data['Close'].iloc[0]) / data['Close'].iloc[0]) * 100
        moving_average = calculate_moving_average(data, period=15)  # 15-day moving average        
        ax1.plot(data.index, ytd_gain, label=f'{label} YTD Gain (%)')
        ax1.plot(data.index, ((moving_average - data['Close'].iloc[0]) / data['Close'].iloc[0]) * 100, 
                 label=f'{label} 15-Day MA', linestyle='--')
    
    ax1.set_title('YTD Gains and Moving Averages')
    ax1.set_ylabel('Gain in %')
    ax1.legend()
    ax1.grid(True)
    
    # Plot volume on the second subplot
    for label, data in stock_data.items():
        ax2.bar(data.index, data['Volume'], label=f'{label} Volume', alpha=0.3)
    
    ax2.set_title('Daily Trading Volume')
    ax2.set_ylabel('Volume')
    ax2.legend()
    ax2.grid(True)
    
    # Global settings and saving
    plt.suptitle(title)
    plt.xlabel('Date')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(file_name)
    plt.show()

# Define the start of the year and the current date
start_date = '2025-01-01'
current_date = datetime.now().strftime('%Y-%m-%d')

# Fetch and plot data for NVDA and TSLA
stock_data = {
    'NVDA': fetch_stock_data('NVDA', start_date, current_date),
    'TSLA': fetch_stock_data('TSLA', start_date, current_date)
}

plot_stock_data(stock_data=stock_data,
                title='Detailed Stock Analysis for NVDA and TSLA in 2025',
                file_name='detailed_ytd_stock_analysis.png')