import yfinance as yf
import pandas as pd
import csv

ids = ['ED', 'DG', 'GIS', 'CHD', 'CPB', 'UNH', 'PM', 'CMS', 'SO', 'KHC', 'WEC', 'ABC', 'KMB', 'DGX', 'PG', 'MKTX', 'LMT', 'PNW', 'WM', 'LNT', 'CNP', 'CNC', 'HOLX', 'ATO', 'CF', 'MKC', 'ABBV', 'BMY', 'TSN', 'CCI', 'ATVI', 'O', 'PGR', 'TIF', 'GILD', 'WLTW', 'AON', 'NI', 'MMC', 'NEE', 'EIX', 'TMUS', 'TRV', 'AJG', 'ALL', 'YUM', 'HCA', 'BRK.B', 'WELL', 'HIG', 'TJX', 'LLY', 'UNM', 'COST', 'WMB', 'EA', 'STE', 'FOXA', 'LIN', 'COG', 'GL', 'LHX', 'GD', 'JNPR', 'REG', 'NVR', 'MDT', 'INCY', 'SRE', 'LKQ', 'BLL', 'DVN', 'COP', 'AKAM', 'AIZ', 'TSCO', 'EBAY', 'ULTA', 'ZBH', 'PKG', 'BIIB', 'CHRW', 'UDR', 'REGN', 'ECL', 'FANG', 'BR', 'ZTS', 'IFF','EXPD', 'UHS', 'OMC', 'TGT', 'FRT', 'FAST', 'NDAQ', 'OKE', 'UNP']

with open('StackWyrms/stocks.csv', 'w', newline = '') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Symbol', 'Name', 'Beta', 'PriceToBook','CurrentPrice'])

    for name in ids:
        stockdata = []
        stock = yf.Ticker(name)
        stockdata.append(stock.info.get('symbol'))
        stockdata.append(stock.info.get('shortName'))
        stockdata.append(stock.info.get('beta'))
        stockdata.append(stock.info.get('priceToBook'))
        stockdata.append(stock.info.get('currentPrice'))
        writer.writerow(stockdata)

def getStockSymbol(symbol):
    df = pd.read_csv("/stocks.csv")
    result = df[df[id_column_name] == symbol]
    return 


'''
stock = yf.Ticker("MSFT")
print(stock.info.get('symbol'))
print(stock.info.get('shortName'))
print(stock.info.get('beta'))
print(stock.info.get('priceToBook'))
print(stock.info.get('currentPrice'))
print("")
'''
