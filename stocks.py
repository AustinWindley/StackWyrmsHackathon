import yfinance as yf
import csv

ids = ['ED', 'DG', 'GIS', 'CHD', 'CPB', 'UNH', 'PM', 'CMS', 'SO', 'KHC', 'WEC', 'ABC', 'KMB', 'DGX', 'PG', 'MKTX', 'LMT', 'PNW', 'WM', 'LNT', 'CNP', 'CNC', 'HOLX', 'ATO', 'CF', 'MKC', 'ABBV', 'BMY', 'TSN', 'CCI', 'ATVI', 'O', 'PGR', 'TIF', 'GILD', 'WLTW', 'AON', 'NI', 'MMC', 'NEE', 'EIX', 'TMUS', 'TRV', 'AJG', 'ALL', 'YUM', 'HCA', 'BRK.B', 'WELL', 'HIG', 'TJX', 'LLY', 'UNM', 'COST', 'WMB', 'EA', 'STE', 'FOXA', 'LIN', 'COG', 'GL', 'LHX', 'GD', 'JNPR', 'REG', 'NVR', 'MDT', 'INCY', 'SRE', 'LKQ', 'BLL', 'DVN', 'COP', 'AKAM', 'AIZ', 'TSCO', 'EBAY', 'ULTA', 'ZBH', 'PKG', 'BIIB', 'CHRW', 'UDR', 'REGN', 'ECL', 'FANG', 'BR', 'ZTS', 'IFF','EXPD', 'UHS', 'OMC', 'TGT', 'FRT', 'FAST', 'NDAQ', 'OKE', 'UNP']

'''
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

def getStockName(symbol):
    with open ('StackWyrms/stocks.csv') as fileObject:
        reader = csv.reader(fileObject)
        for row in reader:
            if row[0] == symbol:
                data = []
                for item in row:
                    data.append(item)
        name = data[1]
        return(name)

def getStockBeta(symbol):
    with open ('StackWyrms/stocks.csv') as fileObject:
        reader = csv.reader(fileObject)
        for row in reader:
            if row[0] == symbol:
                data = []
                for item in row:
                    data.append(item)
        beta = data[2]
        return(beta)

def getStockPandB(symbol):
    with open ('StackWyrms/stocks.csv') as fileObject:
        reader = csv.reader(fileObject)
        for row in reader:
            if row[0] == symbol:
                data = []
                for item in row:
                    data.append(item)
        PandB = data[3]
        return(PandB)
    
def getStockPrice(symbol):
    with open ('StackWyrms/stocks.csv') as fileObject:
        reader = csv.reader(fileObject)
        for row in reader:
            if row[0] == symbol:
                data = []
                for item in row:
                    data.append(item)
        price = data[4]
        return(price)


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
