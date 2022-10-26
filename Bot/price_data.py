import requests
import json
import js2py
import pandas as pd
import datetime
import math

'''
# no need env
KEY = "ckey_cbbfe71b4dbf4d3a942f8dcbd67"

def main(
    TOKEN = "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",
    START = "2022-09-01",
    END = "2022-09-30",
    SIZE = 30):
    PAGE_SIZE = str(SIZE)
    response_API = requests.get(f'https://api.covalenthq.com/v1/pricing/historical_by_addresses_v2/1/USD/'+TOKEN+'/?quote-currency=USD&format=JSON&from='+END+'&to='+START+'&page-size='+PAGE_SIZE+'&key='+KEY)

    APIdata = response_API.text
    parse_json = json.loads(APIdata)
    price = parse_json['data'][0]['prices']
    priceData = {"price": [], "date": []}


    for i in range(0,len(price)):
        priceData['date'].append(price[i]['date'])
        priceData['price'].append(price[i]['price'])
    
    # print(priceData)
    return priceData'''

def retrieveData(nameID, startDate, endDate, page):
    
    page = str(page)
    url = f'https://www.coingecko.com/en/coins/{nameID}/historical_data?start_date={startDate}&end_date={endDate}&page={page}'
    page = requests.get(url)
    dfs = pd.read_html(page.text)
    
    return dfs

# return date as object
def formatDate(date):
    [year,month,day] = date.split('-')
    return datetime.datetime(int(year),int(month),int(day))
    
# @param nameID = coingecko's ID of token
def main(nameID='bitcoin',
    startDate='2022-07-01',
    endDate='2022-10-21'):
    formattedStartDate = formatDate(startDate)
    formattedEndDate = formatDate(endDate)
    difference = formattedEndDate - formattedStartDate
    if (difference.days/60 > 1):
        numOfPages = str(math.ceil(difference.days / 60))
    else:
        numOfPages = str(1)
    dfs = ''
    data = []
    # each page holds only 60 dates of data therefore to loop
    for page in range(1,int(numOfPages) + 1):
        dfs = retrieveData(nameID, startDate, endDate, page)
        # for each data point, append to list
        for j in range(0,len(dfs[0].Close)):
            # first value of close column is always NaN. append data if string
            if (isinstance(dfs[0].Close[j], str)):
                value = float(str(dfs[0].Close[j]).replace('$','').replace(',',''))
                data.append(value)
            # retrieve value for this NaN cell and append value to list
            elif (math.isnan(dfs[0].Close[j])):
                theDate = dfs[0].Date[j]
                thatDate = formatDate(theDate) + datetime.timedelta(days=1)
                thatDate = str(thatDate.year) +'-'+ str(thatDate.month) +'-'+ str(thatDate.day)
                dfsTwo = retrieveData(nameID,theDate,thatDate,1)
                value = float(str(dfsTwo[0].Close[1]).replace('$','').replace(',',''))
                data.append(value)
                
    # data in ascending order of date
    return data.reverse()
    

if __name__ == "__main__":
    # returns price of token in ascending order of date
    main()