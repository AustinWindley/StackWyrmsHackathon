import yfinance as yf
import csv
import os

# Generalizes the path to be openable anywhere
_CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stocks.csv')

# Top 100 company symbol id's
ids = ['ED', 'DG', 'GIS', 'CHD', 'CPB', 'UNH', 'PM', 'CMS', 'SO', 'KHC', 'WEC', 'ABC', 'KMB', 'DGX', 'PG', 'MKTX', 'LMT', 'PNW', 'WM', 'LNT', 'CNP', 'CNC', 'HOLX', 'ATO', 'CF', 'MKC', 'ABBV', 'BMY', 'TSN', 'CCI', 'ATVI', 'O', 'PGR', 'TIF', 'GILD', 'WLTW', 'AON', 'NI', 'MMC', 'NEE', 'EIX', 'TMUS', 'TRV', 'AJG', 'ALL', 'YUM', 'HCA', 'BRK.B', 'WELL', 'HIG', 'TJX', 'LLY', 'UNM', 'COST', 'WMB', 'EA', 'STE', 'FOXA', 'LIN', 'COG', 'GL', 'LHX', 'GD', 'JNPR', 'REG', 'NVR', 'MDT', 'INCY', 'SRE', 'LKQ', 'BLL', 'DVN', 'COP', 'AKAM', 'AIZ', 'TSCO', 'EBAY', 'ULTA', 'ZBH', 'PKG', 'BIIB', 'CHRW', 'UDR', 'REGN', 'ECL', 'FANG', 'BR', 'ZTS', 'IFF','EXPD', 'UHS', 'OMC', 'TGT', 'FRT', 'FAST', 'NDAQ', 'OKE', 'UNP']

'''
# Gets accurate current trade information.
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
'''

# Get Name of a stock with entered symbol.
def getStockName(symbol):
    with open(_CSV_PATH) as fileObject:
        reader = csv.reader(fileObject)
        for row in reader:
            if row[0] == symbol:
                data = []
                for item in row:
                    data.append(item)
        name = data[1]
        return(name)

# Get Beta of a stock with entered symbol.
def getStockBeta(symbol):
    with open(_CSV_PATH) as fileObject:
        reader = csv.reader(fileObject)
        for row in reader:
            if row[0] == symbol:
                data = []
                for item in row:
                    data.append(item)
        beta = data[2]
        return(beta)

# Get PandB of a stock with entered symbol.
def getStockPandB(symbol):
    with open(_CSV_PATH) as fileObject:
        reader = csv.reader(fileObject)
        for row in reader:
            if row[0] == symbol:
                data = []
                for item in row:
                    data.append(item)
        PandB = data[3]
        return(PandB)

# Get Price of a stock with entered symbol.
def getStockPrice(symbol):
    with open(_CSV_PATH) as fileObject:
        reader = csv.reader(fileObject)
        for row in reader:
            if row[0] == symbol:
                data = []
                for item in row:
                    data.append(item)
        price = data[4]
        return(price)

# Gives the infor back given a specific symbol, defaulted to None
def getStockInfo(symbol):
    with open(_CSV_PATH) as fileObject:
        reader = csv.reader(fileObject)
        next(reader)  # skip header
        for row in reader:
            if row[0] == symbol:
                return {
                    'symbol': row[0],
                    'name': row[1],
                    'beta': float(row[2]) if row[2] else None,
                    'price_to_book': float(row[3]) if row[3] else None,
                    'current_price': float(row[4]) if row[4] else None,
                }
    return None

# Returns a imple list of all symbols in the CSV, useful for dropdowns and such
def getAllSymbols():
    symbols = []
    with open(_CSV_PATH) as fileObject:
        reader = csv.reader(fileObject)
        next(reader)  # skip header
        for row in reader:
            symbols.append(row[0])
    return symbols

'''
#DEBUG CODE
name = getStockName('DG')
beta = getStockBeta('DG')
pandb = getStockPandB('DG')
price = getStockPrice('DG')

print(name)
print("")
print(beta)
print("")
print(pandb)
print("")
print(price)
print("")
'''