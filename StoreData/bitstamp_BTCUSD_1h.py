import csv
import datetime

data = dict({'date': [], 'close': []})

def formatDate(date):
    return date.split('-')

def formatD(date):
    [year,month,day] = date.split('-')
    return datetime.datetime(int(year),int(month),int(day))

# @param date yyyy-mm-dd
def getBTC1h(startDate, endDate, filename='Bitstamp_BTCUSD_1h.csv'):
    [startYear, startMonth, startDay] = formatDate(startDate)
    [endYear, endMonth, endDay] = formatDate(startDate)
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        # unix, date, symbol, open, high, low, close, Volume BTC ,Volume USD
        for row in reader:
            # skip first 2 rows as those are headers
            if len(row) == 9 and row[0].isdigit():
                [currYear, currMon, day] = row[1].split('-')
                currDay = day.split(' ')[0]
                startDate = datetime.datetime(int(startYear),int(startMonth),int(startDay))
                currDate = datetime.datetime(int(currYear),int(currMon),int(currDay))
                test = currDate - startDate
                # get date of current row. If reached startDate, break loop
                toEnd = (currDate - startDate).days < 0
                
                if toEnd:
                    break
                else:
                    for i in range(0,9): # 9 columns
                        if (i == 1):
                            data['date'].append(row[1])
                        elif (i == 6):
                            data['close'].append(row[6])
        
        data['date'].reverse()
        data['close'].reverse()
        print(data)
    
    return data

# getBTC1h('2022-10-25','2022-10-26')