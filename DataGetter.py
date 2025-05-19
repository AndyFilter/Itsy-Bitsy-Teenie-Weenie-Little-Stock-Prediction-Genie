# Request format:
# https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={STOCK_NAME}&interval={TIME_INTERVAL}&month={YEAR}-{MONTH}&outputsize=full&apikey=demo
# example: https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&month=2009-01&outputsize=full&apikey=demo

import requests
import os

if not os.path.exists("API_KEY.txt"):
    raise FileNotFoundError("API_KEY.txt file not found. Please create this file with your API key.")

API_KEY = open("API_KEY.txt").read()

# Make a request to the API
def getData(stock, interval, year, month):
    if not API_KEY:
        raise ValueError("API key is not available")
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock}&interval={interval}&month={year}-{month:02d}&outputsize=full&datatype=csv&apikey={API_KEY}"
    #print(url)
    response = requests.get(url)
    data = response.text
    return data

# Request a whole year
def getDataYear(stock, interval, year):
    data = []
    for i in range(1, 13):
        data.append(getData(stock, interval, year, i))
    return data

# Download a whole year and save to separate files into the directory DataSets/STOCK/YEAR
def downloadYear(stock, interval, year):
    import os
    os.makedirs(f"DataSets/{stock}/{year}", exist_ok=True)
    data = getDataYear(stock, interval, year)
    for i in range(len(data)):
        with open(f"DataSets/{stock}/{year}/intraday_{year}_{(i + 1):02d}_{interval}_{stock}.csv", "w") as f:
            f.write(data[i])


print("Starting...")
downloadYear("IBM", "5min", "2020")
