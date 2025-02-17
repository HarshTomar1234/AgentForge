import os
import pandas as pd
import matplotlib.pyplot as plt
from functions import get_stock_prices

def plot_and_save(stock_prices, directory, filename, title='', ylabel=''):
    plt.figure(figsize=(14, 7))
    if isinstance(stock_prices, pd.DataFrame):
        for col in stock_prices.columns:
            plt.plot(stock_prices.index, stock_prices[col], label=col)
        plt.legend()
    else:
        plt.plot(stock_prices.index, stock_prices, label=filename.strip('.png'))
        plt.legend([filename.strip('.png')])
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.savefig(os.path.join(directory, filename))
    plt.close()

# Define the stock symbols and the date range
stock_symbols = ['NVDA', 'TSLA']
start_date = '2025-01-01'
end_date = '2025-02-17'

# Get the stock prices
stock_prices = get_stock_prices(stock_symbols, start_date, end_date)

# Create a directory if it does not exist
directory = '/content/coding'
if not os.path.exists(directory):
    os.makedirs(directory)

# Plot comparisions of both stocks
plot_and_save(stock_prices, directory, 'comparison_plot.png', 'Comparison of NVDA and TSLA Stock Prices', 'Price in USD')

# Plot individual stock movements
for stock in stock_symbols:
    plot_and_save(stock_prices[[stock]], directory, f'{stock}_plot.png', f'{stock} Stock Price Movement', 'Price in USD')

# Plot rolling mean for each stock
window_size = 10  # days for moving average
for stock in stock_symbols:
    rolling_mean = stock_prices[[stock]].rolling(window=window_size).mean()
    plot_and_save(rolling_mean, directory, f'{stock}_rolling_mean.png', f'{stock} {window_size}-Day Moving Average', 'Price in USD')

print(f"All enhanced stock price plots saved in {directory}")